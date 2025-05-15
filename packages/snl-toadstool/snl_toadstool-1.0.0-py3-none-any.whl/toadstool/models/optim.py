"""Model optimization type functions."""

import math
import warnings
from functools import partial

import torch


def LinearWarmup(optim, total_steps, warmup_steps=500, last_epoch=-1, min_lr=0.0):
    """Linearly increase the LR from 0-`warmup_steps` and then linearly decrease it from `warmup_steps`-`total_steps`
    Utilizes LambdaLR.

    Parameters
    ----------
        optim: The optimizer being used (e.g. Adam, etc.)
        total_steps: The total number of steps to run for.
        warmup_steps: Warmup steps during which we increase the learning rate.
        last_epoch: The name is copied from pytorch's LambdaLR parameters, but this is somewhat confusingly named.  Referring to the argument description for CyclicLR (which inherits from same parent) and the actual code of the parent class LRScheduler, this is actually the batch_count.  As such, if you are restarting on the boundary of an actual epoch, this will be (last epoch number) * (length of your training data in batches)
        https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CyclicLR.html#cycliclr
        https://pytorch.org/docs/stable/_modules/torch/optim/lr_scheduler.html#LRScheduler
        min_lr: what is the lowest we let the learning rate go.  Defaults to 0.
    """
    perc_warmup = warmup_steps / total_steps
    if perc_warmup > 0.1:
        warnings.warn(f'Warmup # steps is high {perc_warmup * 100:.2f}%')

    lam = partial(linear_warmup, total_steps=total_steps, warmup=warmup_steps, min_lr=min_lr)
    return torch.optim.lr_scheduler.LambdaLR(optim, lam, last_epoch=last_epoch)


def linear_warmup(cur_step, total_steps, warmup=500, min_lr=0.0):
    if cur_step < warmup:
        return float(cur_step) / float(max(1, warmup))
    return max(min_lr, float(total_steps - cur_step) / float(max(1, total_steps - warmup)))


def LinearWarmupWithCosineDecay(optim, total_steps, warmup_steps=500, last_epoch=-1, min_lr=0.0):
    """Linearly increase the LR from 0-`warmup_steps` and then linearly decrease it from `warmup_steps`-`total_steps`
    Utilizes LambdaLR.

    Parameters
    ----------
        optim: The optimizer being used (e.g. Adam, etc.)
        total_steps: The total number of steps to run for.
        warmup_steps: Warmup steps during which we increase the learning rate.
        last_epoch: The name is copied from pytorch's LambdaLR parameters, but this is somewhat confusingly named.  Referring to the argument description for CyclicLR (which inherits from same parent) and the actual code of the parent class LRScheduler, this is actually the batch_count.  As such, if you are restarting on the boundary of an actual epoch, this will be (last epoch number) * (length of your training data in batches)
        https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CyclicLR.html#cycliclr
        https://pytorch.org/docs/stable/_modules/torch/optim/lr_scheduler.html#LRScheduler
        min_lr: what is the lowest we let the learning rate go.  Defaults to 0.
    """
    perc_warmup = warmup_steps / total_steps
    if perc_warmup > 0.1:
        warnings.warn(f'Warmup # steps is high {perc_warmup * 100:.2f}%')

    lam = partial(linear_warmup_with_cosine_decay, total_steps=total_steps, warmup=warmup_steps, min_lr=min_lr)
    return torch.optim.lr_scheduler.LambdaLR(optim, lam, last_epoch=last_epoch)


def linear_warmup_with_cosine_decay(cur_step, total_steps, warmup=500, min_lr=0.0):
    if cur_step < warmup:
        return float(cur_step) / float(max(1, warmup))
    progress = float(cur_step - warmup) / float(max(1, total_steps - warmup))
    return max(min_lr, 0.5 * (1.0 + math.cos(math.pi * progress)))
