import logging
import math
import time
from pathlib import Path

import torch

from toadstool.models.dl_utils import CancelTrainException

log = logging.getLogger(__name__)


class TrackMemory:
    def __init__(self):
        self.allocd = {}
        self.reserved = {}
        self.init_free, self.total_mem = torch.cuda.mem_get_info()

    def to_perc(self, size):
        return round(100 * (size / self.total_mem), 2)

    def begin_batch(self, trainer):
        self.update_tracker('begin_batch')

    def after_batch(self, trainer):
        self.update_tracker('after_batch')

    def after_backward(self, trainer):
        self.update_tracker('after_backward')

    def after_step(self, trainer):
        self.update_tracker('after_step')

    def after_fit(self, trainer):
        self.print()

    def update_tracker(self, key):
        if key not in self.allocd:
            self.allocd[key] = []
            self.reserved[key] = []
        self.allocd[key].append(torch.cuda.memory_allocated())
        self.reserved[key].append(torch.cuda.memory_reserved())

    def print(self):
        stats = torch.cuda.memory_stats()
        print(f'Device : {torch.cuda.current_device()}')
        print(f'\tAlloc Retries: {stats.get("num_alloc_retries", 0)}')
        print(f'\tooms         : {stats.get("num_ooms", 0)}')
        max_reserved = torch.cuda.max_memory_reserved()
        print(f'\tMax reserved : {self.to_perc(max_reserved)}% - {convert_size(max_reserved)}')
        max_allocd = torch.cuda.max_memory_allocated()
        print(f'\tMax allocd   : {self.to_perc(max_allocd)}% - {convert_size(max_allocd)}')


class TimerCallback:
    def __init__(self, kill_after=None, on_step=True):
        self.timers = {}
        self.kill_on = None
        if kill_after is not None:
            self.kill_on = 'batch' if on_step else 'epoch'
            self.kill_counter = kill_after

    def begin_fit(self, trainer):
        self.start('fit')

    def begin_epoch(self, trainer):
        self.start('epoch')

    def begin_batch(self, trainer):
        self.start('batch')

    def after_batch(self, trainer):
        self.stop('batch')

    def after_epoch(self, trainer):
        self.stop('epoch')

    def after_fit(self, trainer):
        self.stop('fit')

    def start(self, name):
        self.timers[name] = time.perf_counter()

    def stop(self, name):
        if self.kill_on == name:
            self.kill_counter -= 1
            if self.kill_counter == 0:
                raise CancelTrainException()
        print(f'Timer {name}: {round(time.perf_counter() - self.timers[name], 6)}')


class ProfilerCallback:
    def __init__(self, logdir, name):
        self.fn = Path(logdir) / name

        self.is_dist = torch.distributed.is_initialized()
        self.rank = torch.distributed.get_rank()

        self.prof = torch.profiler.profile(
            schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
            on_trace_ready=torch.profiler.tensorboard_trace_handler(self.fn),
            profile_memory=True,
            record_shapes=True,
            with_stack=True,
        )

    def begin_fit(self, trainer):
        self.prof.start()
        self.step = 0

    def after_batch(self, trainer):
        self.prof.step()
        self.step += 1
        if self.step > 15:
            raise CancelTrainException()

    def after_fit(self, trainer):
        self.prof.stop()


def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f'{s} {size_name[i]}'


class DebugCallback:
    """Checks if gradients are being updated and prints memory info.
    Checks loss != 0.
    """

    def __init__(self):
        self.do_once = True

    def begin_fit(self, trainer):
        self.do_once = True
        self.ctx = torch.autograd.detect_anomaly()
        self.ctx.__enter__()

    def after_fit(self, trainer):
        self.ctx.__exit__(None, None, None)

    def begin_batch(self, trainer):
        if self.do_once:
            log.debug('x:')
            self.print_tensor_shape(trainer.x)
            log.debug('y:')
            self.print_tensor_shape(trainer.y)

    def print_tensor_shape(self, x):
        if isinstance(x, torch.Tensor):
            log.debug(f'{x.shape}')
        if isinstance(x, dict):
            for key in x:
                log.debug(f'{key}:')
                self.print_tensor_shape(x[key])
        if isinstance(x, list | tuple):
            for i, xi in enumerate(x):
                log.debug(f'{i}:')
                self.print_tensor_shape(xi)

    def after_pred(self, trainer):
        if self.do_once:
            self.print_tensor_shape(trainer.y_p)

    def after_loss(self, trainer):
        assert trainer.loss != 0

    def after_batch(self, trainer):
        self.do_once = False

    def all_batches(self, trainer):
        self.name_printed = {'infinite': [], 'no_gradient': [], 'unused': []}

    def after_backward(self, trainer):
        self.check_grads(trainer.model)
        check_weight(trainer.model)

    def after_epoch(self, t):
        allocd = torch.cuda.memory_allocated()
        max_allocd = torch.cuda.max_memory_allocated()
        perc = (allocd / max_allocd) * 100
        log.debug(f'Memory usage at epoch {t.epoch} {allocd}/{max_allocd} = {perc:.2f}%')

    def check_grads(self, model):
        for name, param in model.named_parameters():
            if 'weight' in name:
                if param.grad is not None:
                    if not torch.isfinite(param.grad).any() and name not in self.name_printed['infinite']:
                        log.error(f'{name} gradients are infinite')
                        self.name_printed['infinite'].append(name)
                else:
                    if name not in self.name_printed['no_gradient']:
                        log.error(f'Layer {name} has no gradient')
                        self.name_printed['no_gradient'].append(name)
                    continue
                if name not in self.name_printed['unused']:
                    perc_unused = (param.grad == 0).sum() / param.grad.numel()
                    if perc_unused > 0.5:
                        log.debug(f'Layer {name} may not be being used, {perc_unused * 100:.2f}%')
                        self.name_printed['unused'].append(name)


def check_weight(model):
    for name, mod in model.named_modules():
        if hasattr(mod, 'weight') and not torch.isfinite(mod.weight).any():
            log.error(f'{name} weights are infinite')


def watch_layer_shapes(t):
    for m in t.model.modules():
        m.register_forward_hook(layer_hook)
        m.register_backward_hook(layer_hook)


def layer_hook(mod, inp, outp):
    if hasattr(mod, 'weight') and mod.weight.isnan().any():
        log.debug(f'{mod} weight')
    if isinstance(inp[0], dict):
        return
    if inp[0].isnan().any():
        log.debug(f'{mod} inp')
    if outp[0].isnan().any():
        log.debug(f'{mod} outp')
