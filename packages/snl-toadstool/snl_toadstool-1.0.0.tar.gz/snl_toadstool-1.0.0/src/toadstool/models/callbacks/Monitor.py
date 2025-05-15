import logging
import time
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torch.distributed as dist
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy

try:
    # https://discuss.pytorch.org/t/error-while-multiprocessing-in-dataloader/46845/15
    # ^ doing tqdm.auto causes a problem for some reason
    from tqdm import tqdm
except ImportError:
    tqdm = None


class SimpleMonitorCallback:
    """Records loss values and prints them for each epoch."""

    def __init__(self, verbose=True):
        self.verbose = verbose

    def begin_epoch(self, trainer):
        self.start = time.time()
        self.train_losses = [0, 0]
        self.valid_losses = [0, 0]

    def after_loss(self, trainer):
        loss = trainer.loss.cpu().detach()
        if trainer.model.training:
            self.train_losses[0] += loss
            self.train_losses[1] += 1
        if not trainer.model.training:
            self.valid_losses[0] += loss
            self.valid_losses[1] += 1

    def after_epoch(self, trainer):
        if not self.verbose:
            return
        print(f'Epoch: {trainer.epoch} - {time.time() - self.start:.2f} s')
        print(f'\ttrain: {self.train_losses[0]:.4f} : {self.train_losses[0] / self.train_losses[1]:.4f}')
        print(f'\tvalid: {self.valid_losses[0]:.4f} : {self.valid_losses[0] / self.valid_losses[1]:.4f}')
        if hasattr(trainer, 'score'):
            print(f'\tscore: {trainer.score:.2f}')

    def cancelled_training(self, trainer):
        print('Training cancelled')


# WARNING: if you don't do begin_fit on some of these they will crash


class MonitorCallback:
    """Records loss values and prints them for each epoch."""

    def __init__(self, track_lr=False, level=logging.INFO):
        self.track_lr = track_lr
        self.log = logging.getLogger('MonitorCallback')
        self.log.setLevel(level)
        if not self.log.hasHandlers():
            self.log.addHandler(logging.StreamHandler())
        self.losses = {}
        self.stage = None

        self.is_dist = torch.distributed.is_initialized()
        self.rank = 0 if not self.is_dist else torch.distributed.get_rank()

    def begin_fit(self, trainer):
        if self.rank == 0:
            self.stage = 'train'
            self.__add_loss('train')
            self.__add_loss('valid')
            if self.track_lr:
                self.lrs = [[] for _ in trainer.opt.param_groups]

    def begin_validate(self, trainer):
        if self.rank == 0:
            self.stage = 'valid'

    def after_validate(self, trainer):
        if self.rank == 0:
            self.stage = 'train'

    def begin_eval(self, trainer):
        if self.rank == 0:
            self.stage = 'eval'
            self.__add_loss(self.stage)

    def begin_epoch(self, trainer):
        if self.rank == 0:
            self.__start_time = time.time()
            self.__start_tidx = len(self.losses['train'])
            self.__start_vidx = len(self.losses['valid'])

    def all_batches(self, trainer):
        if self.rank == 0 and tqdm:
            trainer.dataloader = tqdm(trainer.dataloader, dynamic_ncols=True)

    def after_loss(self, trainer):
        loss = trainer.loss.detach().clone()
        if self.is_dist:
            torch.distributed.all_reduce(loss, op=torch.distributed.ReduceOp.SUM)

        if self.rank == 0:
            loss = loss.cpu().unsqueeze(0)
            if self.stage is not None:
                self.losses[self.stage] = torch.cat((self.losses[self.stage], loss), 0)

            if self.track_lr and self.stage == 'train':
                for pg, lr in zip(trainer.opt.param_groups, self.lrs):
                    lr.append(pg['lr'])

    def __add_loss(self, name):
        if self.rank == 0 and name not in self.losses:
            self.losses[name] = torch.Tensor()

    def after_epoch(self, trainer):
        if self.rank == 0:
            epoch_tloss = self.losses['train'][self.__start_tidx :]
            epoch_vloss = self.losses['valid'][self.__start_vidx :]

            self.log.info(f'Epoch: {trainer.epoch} - {time.time() - self.__start_time:.2f} s')
            self.log.info(f'\ttrain: {epoch_tloss.sum():.4f} : {epoch_tloss.mean():.4f}')
            self.log.info(f'\tvalid: {epoch_vloss.sum():.4f} : {epoch_vloss.mean():.4f}')
            if hasattr(trainer, 'score'):
                self.log.info(f'\tscore: {trainer.score}')

    def cancelled_training(self, trainer):
        if self.rank == 0:
            self.log.info('Training cancelled')

    def plot_lr(self, pgid=-1):
        plt.plot(self.lrs[pgid])

    def plot_loss(self, stage):
        plt.plot(self.losses[stage].numpy())

    def plot(self, skip_last=5, pgid=-1):
        plt.xscale('log')
        plt.plot(self.lrs[pgid][:-skip_last], self.losses['train'][:-skip_last].numpy())


try:
    from torch.utils.tensorboard import SummaryWriter

    class TensorBoardCallback:
        """Writes loss and evaluation values on tensorboard.

        Parameters
        ----------
            logdir: string or os.path
                Directory to write Tensorboard information
            name: string or os.oath
                Filename to write Tensorboard information
            extra_attributes: list<string>
                list of strings of names of attributes to search trainer object for
                    and if available also plot after each epoch.
            on_step: int
                Instead of checking extra_attributes on each epoch, check them every
                    on_step
            start_train_step: int
                When reloading can set the current step so we write to the log correctly
            start_valid_step: int
                Same with the validation charts

        """

        def __init__(self, logdir, name, extra_attributes=None, start_train_step=0, start_valid_step=0):
            if extra_attributes is None:
                extra_attributes = ['score']
            self.fn = str(Path(logdir) / name)
            self.writer = None
            self.extra_attrs = extra_attributes

            self.is_dist = torch.distributed.is_initialized()
            self.rank = torch.distributed.get_rank() if self.is_dist else 0
            self.train_step = start_train_step
            self.valid_step = start_valid_step

        def begin_fit(self, trainer):
            if self.writer is not None:
                self.writer.close()
            if self.rank == 0:
                self.writer = SummaryWriter(self.fn)

                self.epoch_loss = 0
                self.epoch_valid_loss = 0

        def after_fit(self, trainer):
            if self.writer is not None:
                self.writer.close()

        def after_loss(self, trainer):
            loss = trainer.loss.detach().clone()
            if self.is_dist:
                torch.distributed.all_reduce(loss, op=torch.distributed.ReduceOp.AVG)
            # .float() to convert from possibly b16
            loss = loss.float().cpu()

            if trainer.model.training and self.rank == 0:
                self.epoch_loss += loss
                self.writer.add_scalar('train_loss', loss, self.train_step)
                self.train_step += 1
            if not trainer.model.training and self.rank == 0:
                self.epoch_valid_loss += loss
                self.writer.add_scalar('valid_loss', loss, self.valid_step)
                self.valid_step += 1

        def begin_optim(self, trainer):
            if isinstance(trainer.model, FSDP):
                grad_norm = get_grad_norm_fsdp(trainer.model)
            else:
                grad_norm = get_grad_norm_local(trainer.model)
            if self.rank == 0:
                self.writer.add_scalar('grad_norm', grad_norm, self.train_step)

        def after_step(self, trainer):
            if self.rank == 0:
                if hasattr(trainer, 'lr'):
                    self.writer.add_scalar('learning_rate', trainer.lr, self.train_step)
                for i, pg in enumerate(trainer.opt.param_groups):
                    self.writer.add_scalar(f'learning_rate_{i}', pg['lr'], self.train_step)

        def after_epoch(self, trainer):
            if self.rank == 0:
                self.writer.add_scalar('epoch_loss', self.epoch_loss / self.train_step, trainer.epoch)
                if self.valid_step > 0:
                    self.writer.add_scalar('epoch_valid_loss', self.epoch_valid_loss / self.valid_step, trainer.epoch)
                self.epoch_loss = 0
                self.epoch_valid_loss = 0
                self.train_step = 0
                self.valid_step = 0

                for attr in self.extra_attrs:
                    if hasattr(trainer, attr):
                        self.writer.add_scalar(attr, getattr(trainer, attr), trainer.epoch)
except ImportError:
    pass


def get_grad_norm_fsdp(model, sharding_strategy=ShardingStrategy.FULL_SHARD):
    local_norm = get_grad_norm_local(model)
    return_norm = local_norm.clone().detach().requires_grad_(False).to(local_norm.device) ** 2
    dist.all_reduce(return_norm, op=torch.distributed.ReduceOp.SUM)
    if sharding_strategy == ShardingStrategy.NO_SHARD:
        return_norm = return_norm / dist.get_world_size()
    return return_norm**0.5


def get_grad_norm_local(model):
    total_norm = 0.0
    for p in model.parameters():
        if p.grad is not None:
            local_norm = torch.linalg.vector_norm(p.grad, dtype=p.dtype)
            total_norm += local_norm**2
    return total_norm**0.5
