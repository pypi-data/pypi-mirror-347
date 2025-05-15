import matplotlib.pyplot as plt
import numpy as np
import scipy
import torch
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

from toadstool.models.dl_utils import CancelTrainException


class GradClipCallback:
    """Clip gradients before optimization step."""

    def __init__(self, threshold=1):
        """Threshold == max_norm."""
        self.clip = threshold

    def begin_optim(self, trainer):
        trainer.scaler.unscale_(trainer.opt)
        if isinstance(trainer.model, FSDP):
            trainer.model.clip_grad_norm_(self.clip)
        else:
            torch.nn.utils.clip_grad_norm_(trainer.model.parameters(), self.clip)


class LRSchedulerCallback:
    """Generic PyTorch learning scheduler holder.
    It should be setup (i.e. optimizer passed to it) before here.

    Parameters
    ----------
    scheduler:
        Scheduler to use, should already be setup
    on_step: bool
        Whether to call scheduler.step on after_epoch or after_step
    """

    def __init__(self, scheduler, on_step=True):
        self.scheduler = scheduler
        if on_step:
            self.after_step = self.step
        else:
            self.after_epoch = self.step

    def step(self, trainer):
        self.scheduler.step()
        trainer.lr = self.scheduler.get_last_lr()[0]

    def state_dict(self):
        return self.scheduler.state_dict()

    def load_state_dict(self, state_dict):
        self.scheduler.load_state_dict(state_dict)


class LRFinderCallback:
    """exponentially increases learning rate for max_iters and plots the losses."""

    def __init__(self, max_iter=100, min_lr=1e-6, max_lr=10):
        self.max_iter, self.min_lr, self.max_lr = max_iter, min_lr, max_lr
        self.best_loss = 1e9

    def begin_fit(self, trainer):
        self.n_iter = 0
        self.lrs = [[] for _ in trainer.opt.param_groups]
        self.losses = torch.Tensor()

    def begin_batch(self, trainer):
        if not trainer.model.training:
            return

        pos = self.n_iter / self.max_iter
        lr = self.min_lr * (self.max_lr / self.min_lr) ** pos

        for pg in trainer.opt.param_groups:
            pg['lr'] = lr
        self.n_iter += 1

    def after_loss(self, trainer):
        if not trainer.model.training:
            return
        loss = trainer.loss.cpu().detach().unsqueeze(0)
        self.losses = torch.cat((self.losses, loss), 0)

        for pg, lr in zip(trainer.opt.param_groups, self.lrs):
            lr.append(pg['lr'])

    def after_step(self, trainer):
        if self.n_iter >= self.max_iter or trainer.loss.item() > self.best_loss * 10:
            raise CancelTrainException()
        self.best_loss = min(trainer.loss.item(), self.best_loss)

    def plot_lr(self, pgid=-1):
        plt.plot(self.lrs[pgid])

    def plot_loss(self, stage):
        plt.plot(self.losses[stage].numpy())

    def plot(self, skip_first=5, skip_last=5, pgid=-1):
        x = self.lrs[pgid][skip_first:-skip_last]
        y = self.losses[skip_first:-skip_last]
        y = scipy.interpolate.UnivariateSpline(x, y)(x)
        plt.xscale('log')
        plt.plot(x, y)
        recommend = best_loss(y)
        plt.plot(x[recommend], y[recommend], markersize=10, marker='o', color='red')
        return x[recommend]


def best_loss(losses, penalty=5):
    """Find the most downwardly part of the losses and grab the steepest gradient.

    Calculates it by finding the max subarray of gradient sign values where positive gradients
        are treated as -`penalty` rather than 0
    """
    grads = np.gradient(losses)
    numbers = (grads < 0).astype(np.int32)
    numbers[numbers == 0] = -penalty
    res = max_subarray(numbers)
    return grads[res[0] : res[1]].argmin()
    # return (res[0]+res[1])//2


def max_subarray(numbers):
    """Find a contiguous subarray with the largest sum."""
    best_sum = 0  # or: float('-inf')
    best_start = best_end = 0  # or: None
    current_sum = 0
    for current_end, x in enumerate(numbers):
        if current_sum <= 0:
            # Start a new sequence at the current element
            current_start = current_end
            current_sum = x
        else:
            # Extend the existing sequence with the current element
            current_sum += x

        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_end = current_end + 1  # the +1 is to make 'best_end' exclusive

    return best_start, best_end
