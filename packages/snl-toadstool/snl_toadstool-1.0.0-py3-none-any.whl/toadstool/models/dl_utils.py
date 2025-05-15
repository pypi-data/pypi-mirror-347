"""Code to make Deep Learning easier."""

import importlib
import logging
from contextlib import ExitStack
from functools import partial

import torch
from torch.amp import GradScaler, autocast
from torch.distributed.fsdp import FullStateDictConfig, OptimStateKeyType, StateDictType
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.sharded_grad_scaler import ShardedGradScaler
from torch.nn import DataParallel
from torch.nn.parallel import DistributedDataParallel as DDP

log = logging.getLogger(__name__)


class CantTrainException(Exception):
    pass


class CancelTrainException(Exception):
    pass


class Trainer:
    """
    Provides helper functions for running data through a model e.g. training.
    Exposes most data to arbitrary Callback handlers manipulation/monitoring.

    Also catches certain custom Exceptions for control flow.

    Parameters
    ----------
        model: torch.nn.Module
            The model.
            Should accept the first tuple of the dataloader during `.fit`

        optimizer: torch.optim.Optimizer

        loss_func: function(yp, y)
            yp is the output from the model.
            y is the second output from the dataloader during `.fit`

        callbacks:
            Callback handlers are expected to be classes with function names
                that match one of the "Hooks" throughout the
                training process, and accept this `Trainer` object as the only
                parameter.
            ``` Example
            class Callback():
                def begin_fit(self, trainer):
                    pass
                def begin_epoch(self, trainer):
                    pass
                ...
            ```
            The callback is then expected to read or ALTER any "State Data" in
                the `Trainer` object.
            There are also various conditional variables that can control the
                training process.
            **Note** Each epoch has "2" `all_batch()` calls.
                One for training and one for validation since I imagine always doing it.
                    Use .model.training to determine which stage it is in.
                **Callbacks are called in the order they are in the list.**
        use_amp: bool
            Whether to use Automatic Mixed Precision
        opt_to_none: bool
            Param for self.opt.zero_grad(set_to_none=opt_to_none)

    Hooks
    -----
        `begin_fit`, `after_fit`: Start and end of training
        `begin_epoch`, `after_epoch`: Start and end of each Epoch
        `begin_batch`, `after_batch`: Start and end of each batch
        `begin_valid`, `after_valid`: After each training epoch a validation epoch is run
        `begin_predict`, `after_predict`: Start and end of calling .predict
        `begin_eval`, `after_eval`: Start and end of calling .eval

        `all_batches`: When .all_batches method is called
        `after_pred`: After the model returns prediction of current batch
        `after_loss`: After loss calculation of current batch
        `after_backward`: After loss.backward() call
        `begin_optim`: Before optimizer .step() and .zero_grad() call
        `after_step`: After optimizer .step() call
        `cancelled_training`: Called when CancelTrainException is caught

    Exposed Data
    ------------
        .x, .y: `begin_batch`
            Set during `one_batch` iteration for the current x and y values of
                the data to be fed into the model and then results compared
                against. (Example: CudaCallback transfers these to the gpu)
        .y_p: `after_pred`
            Each `.y_p` is set during `one_batch()` and is the model output.
        .loss: `after_loss`
            The calculated loss of current batch is stored here
        .epoch: `begin_epoch`, `after_epoch`
            The current epoch #
        .model: `begin_fit`
            The current model being trained
        .optimizer:
            The used optimizer and parameters
        .loss_func:
            The used loss function and parameters
        .dataloader: `all_batches`
            Set and used in `all_batches` function (currently used to support tqdm wrapping)

    Conditional Control
    -------------------
        Control of learning can also happen through the use of Exceptions

        CancelTrainException:
            fit function is surrounded by a try/except for this Exception.

    Implementation Details
    ----------------------
        The callbacks are tightly coupled with this class.
        run_callbacks(<string>) will search the callback classes for a function
            names <string> and pass itself to it.
        The <string> should be indicative of when the callback is happening.
        The callbacks then can manipulate any of the exposed state of the Trainer
            through the various variables.

    Example
    -------
        See: `CudaCallback`, `MonitorCallback`, or `EarlyStopping`
    """

    def __init__(
        self, model, optimizer, loss_function, callbacks=None, use_amp=False, opt_to_none=False, amp_device='cuda'
    ):
        self.model = model
        self.opt = optimizer
        self.loss_func = loss_function
        self.cbs = callbacks if callbacks is not None else []
        self._use_amp = use_amp
        self.amp_device = amp_device
        self.opt_to_none = opt_to_none

        if isinstance(model, FSDP):
            self.scaler = ShardedGradScaler(enabled=self._use_amp or model.mixed_precision.param_dtype == torch.float16)
        else:
            self.scaler = GradScaler(enabled=self._use_amp)
        self.acc_grads = 1

    def fit(self, epochs, train_loader, eval_loader=None, accumulate_gradients=1):
        """
        Training loop.

        Parameters
        ----------
            epochs: int
                number of times to run through `train_loader`
            train_loader: DataLoader
                should return (x,y) values to be fed into model,
                and the loss function respectively
            eval_loader: DataLoader
                same as train_loader, but containing data used for validation
            accumulate_gradients: int > 0
                Number of batches to process before actually taking a gradient step
        """
        if self.opt is None or self.loss_func is None:
            error = f'optimizer {self.opt} or loss func {self.loss_func} is None'
            raise CantTrainException(error)

        self.epochs, self.train_loader, self.eval_loader = epochs, train_loader, eval_loader
        self.acc_grads = accumulate_gradients

        try:
            self.run_callbacks('begin_fit')
            for epoch in range(epochs):
                self.epoch = epoch
                self.run_callbacks('begin_epoch')
                self.model.train()
                self.all_batches(train_loader)
                if eval_loader is not None:
                    self.eval(eval_loader, _stage_name='validate')
                self.run_callbacks('after_epoch')
        except (CancelTrainException, KeyboardInterrupt):
            self.run_callbacks('cancelled_training')
        finally:
            self.run_callbacks('after_fit')

    def eval(self, dataloader, _stage_name='eval'):
        """
        Run data through the model without accumulating gradients.
        Typically called if you have new data with labels you want to "eval"uate against.

        Parameters
        ----------
            dataloader: DataLoader
                should return (x,y) values to be fed into model. (See: `fit` and `predict`)
            _stage_name: str
                Since validation stage during training uses this, but this also might be called externally:
                    _stage_name allows customizing the callback functions used.
        """
        restore_val = self.model.training

        self.model.eval()
        self.run_callbacks(f'begin_{_stage_name}')
        with torch.no_grad():
            self.all_batches(dataloader)

        self.model.train(restore_val)
        self.run_callbacks(f'after_{_stage_name}')

    def predict(self, dataloader):
        """
        Run data through the model without accumulating gradients and don't expect a y value.

        Parameters
        ----------
            dataloader: DataLoader
                should only return `x` values
        """
        restore_val = self.model.training

        self.model.eval()
        self.run_callbacks('begin_predict')
        with torch.no_grad():
            for i, x in enumerate(dataloader):
                self.one_batch(x, None, i)
        self.model.train(restore_val)
        self.run_callbacks('after_predict')

    def all_batches(self, dataloader):
        """Loop through a whole Dataloader."""
        self.dataloader = dataloader
        self.run_callbacks('all_batches')
        for i, (x, y) in enumerate(self.dataloader):
            self.one_batch(x, y, i)

    def one_batch(self, x, y, i=0):
        """Run one batch through the model."""
        with autocast(device_type=self.amp_device, enabled=self._use_amp):
            self.x, self.y = x, y
            self.run_callbacks('begin_batch')
            self.y_p = self.model(self.x)
            self.run_callbacks('after_pred')
            if self.y is not None and self.loss_func is not None:
                self.loss = self.loss_func(self.y_p, self.y)
                self.run_callbacks('after_loss')
                self.loss = self.loss / self.acc_grads
            else:
                self.loss = None
        if self.model.training:
            self.scaler.scale(self.loss).backward()
            self.run_callbacks('after_backward')
            if (i % self.acc_grads) == 0:
                self.run_callbacks('begin_optim')
                self.scaler.step(self.opt)
                self.run_callbacks('after_step')
                self.scaler.update()
                self.opt.zero_grad(set_to_none=self.opt_to_none)
        self.run_callbacks('after_batch')

    def run_callbacks(self, cb_name):
        """Loops over all Callbacks and finds function corresponding to cb_name and calls it."""
        for cb in self.cbs:
            f = getattr(cb, cb_name, None)
            if f:
                f(self)

    def __repr__(self):
        num_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        return f'{self.__class__.__name__}\n\tModel: {num_params}\n{self.model}\n\tCallbacks: {self.cbs}\n\tOpt: {self.opt}\n\tLoss: {self.loss_func}'

    def checkpoint(self, fn, meta=None):
        """Saves just the model and optimizer state along with meta data."""
        # save handles FSDP internally
        self.save(fn, unwrap_model=False, save_opt=True, save_loss_func=False, save_cbs=False, meta_data=meta)

    def load_checkpoint(self, fn):
        """Just loads the model and optimizer state and returns meta data."""
        if fn is None:
            raise ValueError('Passed filename is None')

        save_dict = torch.load(fn, map_location='cpu')

        with ExitStack() as stack:
            opt_state = save_dict['opt']['state']
            if isinstance(self.model, FSDP):
                stack.enter_context(FSDP.state_dict_type(self.model, StateDictType.FULL_STATE_DICT))
                opt_state = FSDP.shard_full_optim_state_dict(opt_state, self.model)

            self.model.load_state_dict(save_dict['model']['state'])
            self.opt.load_state_dict(opt_state)
            self.scaler.load_state_dict(save_dict['amp']['scaler']['state'])

            for cb in self.cbs:
                cb_name = cb.__module__
                if hasattr(cb, 'load_state_dict') and cb_name in save_dict['cbs']:
                    print('Found cb state_dict')
                    cb.load_state_dict(save_dict['cbs'][cb_name]['state'])

        return save_dict['meta_data']

    def save(
        self,
        name,
        *,
        unwrap_model=True,
        model_args=None,
        model_kwargs=None,
        opt_kwargs=None,
        save_opt=True,
        save_loss_func=True,
        save_cbs=False,
        meta_data=None,
    ):
        """
        Serialize and save a Trainer object.
        Saves the model and optimizer state_dict, loss function and optionally
            the callbacks along with generic meta_data.

        Parameters
        ----------
            name: string
                filename path to save serialized object to
            unwrap_model: bool
                If the model state_dict should be unwrapped from FSDP and DDP
                    if it is FSDP then model_args or model_kwargs needs to be supplied to create an unwrapped model for saving optimizer state
            model_args: list
                args to pass to model to recreate it.
                If this and kwargs is None then you must pass a created `model` into load to load it again
                If you don't need args or kwargs, pass an empty list or dict, i.e., `model_args=[]` or `model_kwargs={}`
            model_kwargs: dict
                kwargs that need to be passed to the model to recreate it.
                If None you must pass a created `model` into load to load it again
            opt_kwargs: dict
                If save_opt == True, these are the arguments set to initialize the optimizer.
                Must be set if the optimizer requires them on load.
            save_opt: boolean
                Whether to save the optimizer.
            save_loss_func: boolean
                Whether to save the loss function.
            save_cbs: boolean
                Whether to save the callback list.
                Definitely don't want to if you can't reload them.
            meta_data: * (default: dict)
                Any extra data you want written alongside the object.

        WARNING: ensure meta_data is serializable.
        """
        if torch.distributed.is_initialized():
            rank = torch.distributed.get_rank()
        else:
            rank = 0

        if meta_data is None:
            meta_data = {}
        save_model = model_args is not None or model_kwargs is not None
        save_opt = self.opt is not None and save_opt

        # save misc stuff and create the save_dict
        save_dict = {'model': {}, 'meta_data': meta_data}

        if self.loss_func is not None and save_loss_func:
            save_dict['loss_func'] = self.loss_func
        if save_cbs and self.cbs:
            save_dict['cbs'] = self.cbs

        # Save amp things
        save_dict['amp'] = {'enabled': self._use_amp}
        save_dict['amp']['scaler'] = {'state': self.scaler.state_dict()}

        # Save the model and optimizer
        model_obj = self.model
        model_state = None
        opt_state = None
        if isinstance(self.model, FSDP):
            # Allows the call to model.state_dict() to behave as defined here
            save_policy = FullStateDictConfig(offload_to_cpu=True, rank0_only=True)
            with FSDP.state_dict_type(self.model, StateDictType.FULL_STATE_DICT, save_policy):
                model_state = self.model.state_dict()
                opt_state = FSDP.full_optim_state_dict(self.model, self.opt, rank0_only=True) if save_opt else None
                if rank == 0 and unwrap_model:
                    if save_model:
                        model_obj = self.model.module
                        unwrapped_model = reconstruct_obj(save_object(model_obj, model_args, model_kwargs))
                        opt_state = (
                            FSDP.rekey_optim_state_dict(opt_state, OptimStateKeyType.PARAM_ID, unwrapped_model)
                            if save_opt
                            else None
                        )
                    else:
                        # We don't fail here because they can still load it again by manually recreating the model
                        log.exception(
                            'Unable to reconstruct model without provided arguments. '
                            'Saving the wrapped model. You will have to recreate the wrapped model to load it'
                        )
        else:
            if unwrap_model and isinstance(self.model, DataParallel | DDP):
                model_state = self.model.module.state_dict()
                model_obj = self.model.module
            else:
                model_state = self.model.state_dict()
                model_obj = self.model
            opt_state = self.opt.state_dict() if save_opt else None

        save_dict['model']['state'] = model_state
        if save_model:
            save_dict['model'].update(save_object(model_obj, model_args, model_kwargs))
        if save_opt:
            save_dict['opt'] = save_object(self.opt, kwargs=opt_kwargs)
            save_dict['opt']['state'] = opt_state

        # Save callback information if needed, such as for LR schedulers
        save_dict['cbs'] = {}
        for cb in self.cbs:
            cb_name = cb.__module__
            if hasattr(cb, 'state_dict'):
                save_dict['cbs'][cb_name] = {}
                save_dict['cbs'][cb_name]['state'] = cb.state_dict()

        # Only one place should be saving the model, but FSDP has to have all processes call the `state_dict()` functions
        if rank == 0:
            torch.save(save_dict, name)
        if torch.distributed.is_initialized():
            torch.distributed.barrier()

    @classmethod
    def load(cls, name, model, device=torch.device('cpu'), wrap_model=None):  # noqa B008
        """
        Load a previously saved Trainer (or subclass).

        Parameters
        ----------
            name: string
                filename path of saved Trainer object.
                Format expected to be that of `Trainer.save()`
            model: nn.Module | None
                A PyTorch Module that will accept the 'model_state' state_dict.
                OR
                None, and it will attempt to recreate the model from saved information (This will call importlib on the saved module and class).
            device: torch.device
                what device to load the model onto
            wrap_model: Callable
                Something like DDP or FSDP so it can call FSDP(model)

        Returns
        -------
            Trainer: Type[Trainer]
                The Trainer class
            meta_data: * (probably a dict)
                Whatever meta_data was passed to `save`
        """
        # https://github.com/pytorch/pytorch/issues/2830
        #   optimizer is supposed to be constructed with the model parameters set
        # map to cpu just for compatibility
        #   when the state_dicts are loaded they will be transferred to appropriate gpu
        save_dict = torch.load(name, map_location=device)

        # Load the model
        model_state = save_dict['model']['state']
        if model is None:
            try:
                model = reconstruct_obj(save_dict['model'])
            except TypeError as e:
                raise TypeError(
                    'Did you mean to save with `unwrap_model=True?`'
                    'If so you will have to recreate the wrapped object and pass in `load(model=<wrapped_model>)`'
                ) from e
            except KeyError as e:
                raise KeyError(
                    'Model information was probably not saved to be able to automatically recreate it.'
                ) from e
        elif 'module' in save_dict['model']:
            log.error('Model obj was saved, but model was provided, defaulting to use the provided model')
        model.load_state_dict(model_state)
        model.to(device)

        if wrap_model is not None:
            # If FSDP could do something more performant with `sync_module_states`
            model = wrap_model(model, device)

        # Load the optimizer
        opt = None
        if 'opt' in save_dict:
            opt = reconstruct_obj(save_dict['opt'], more_args=[model.parameters()])

            state = save_dict['opt']['state']
            if isinstance(model, FSDP):
                state = FSDP.shard_full_optim_state_dict(state, model, optim=opt)
            opt.load_state_dict(state)

        # Load the rest
        loss_func = save_dict.get('loss_func', None)
        cbs = save_dict.get('cbs', None)
        # If we saved the cbs they should already have their state dicts so no need to reload here

        t = cls(model, opt, loss_func, cbs, save_dict['amp']['enabled'])
        t.scaler.load_state_dict(save_dict['amp']['scaler']['state'])

        return t, save_dict['meta_data']

    @staticmethod
    def clean(name, remove_meta):
        """Remove unnecessary parts from the save file."""
        save_dict = torch.load(name, map_location=torch.device('cpu'))
        if 'opt' in save_dict:
            del save_dict['opt']
        if 'cbs' in save_dict:
            del save_dict['cbs']
        if 'loss_func' in save_dict:
            del save_dict['loss_func']
        if remove_meta:
            save_dict['meta_data'] = {}

        torch.save(save_dict, name)


def convert_from_fsdp(fn, nonwrapped_model):
    assert not isinstance(nonwrapped_model, FSDP)
    if not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0:
        rekey_optimizer(fn, nonwrapped_model, conversion=OptimStateKeyType.PARAM_ID)


def convert_to_fsdp(fn, nonwrapped_model):
    assert not isinstance(nonwrapped_model, FSDP)
    if not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0:
        rekey_optimizer(fn, nonwrapped_model, conversion=OptimStateKeyType.PARAM_NAME)


def rekey_optimizer(fn, nonwrapped_model, conversion=OptimStateKeyType.PARAM_NAME):
    save_dict = torch.load(fn, map_location=torch.device('cpu'))
    save_dict['opt']['state'] = FSDP.rekey_optim_state_dict(save_dict['opt']['state'], conversion, nonwrapped_model)
    torch.save(save_dict, fn)


def save_object(obj, args=None, kwargs=None):
    """Save an object in a way that we can reconstruct it without having to pickle the logic."""
    ret = {}
    ret['module'] = obj.__module__
    ret['class'] = obj.__class__.__name__
    ret['args'] = args if args is not None else []
    ret['kwargs'] = kwargs if kwargs is not None else {}
    return ret


def reconstruct_obj(save_dict, more_args=None, more_kwargs=None):
    if more_args is None:
        more_args = []
    if more_kwargs is None:
        more_kwargs = {}
    args = more_args + save_dict['args']
    kwargs = {}
    kwargs.update(save_dict['kwargs'])
    kwargs.update(more_kwargs)

    cls = load_class(save_dict['module'], save_dict['class'])
    return cls(*args, **kwargs)


def load_class(module_name, class_name):
    """Return the class reference to create new objects."""
    module = importlib.__import__(module_name, fromlist=[class_name])
    return getattr(module, class_name)


class Hook:
    """
    Helper object to register hooks into a module.
        Useful so you have an object to attach things to.
    """

    def __init__(self, module, func):
        """
        Parameters
        ----------
        module: torch.Module
            module to call .register_forward_hook on
        func: Callable<hook: Hook, mod: torch.Module, input: torch.Tensor, output: torch.Tensor>
            function to register as forward hook on module
        """
        self.hook = module.register_forward_hook(partial(func, self))

    def remove(self):
        self.hook.remove()

    def __del__(self):
        self.remove()
