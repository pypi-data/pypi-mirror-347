"""Model initialization functions."""

import functools
import operator

import torch
from torch import nn

from .dl_utils import Hook


# Used for finding all certain layers, to register hooks
def get_modules(module, cond):
    """Find all layers with module that matches a condition.

    Parameters
    ----------
    module: torch.nn.Module
    cond: Callable[[torch.nn.Module], bool]
    """
    if cond(module):
        return [module]
    return functools.reduce(operator.iadd, [get_modules(layer, cond) for layer in module.children()], [])


def append_stat(hook, mod, inp, outp):
    d = outp.data
    hook.mean, hook.std = d.mean().item(), d.std().item()


def lsuv_module(model, m, xb):
    h = Hook(m, append_stat)

    # - .5 because the mean of relu can't be 0
    while model(xb) is not None and abs(h.mean) - 0.5 > 1e-3:
        m.bias -= h.mean
    while model(xb) is not None and abs(h.std - 1) > 1e-3:
        m.weight.data /= h.std

    h.remove()
    return h.mean, h.std


def lsuv_init(model, dataloader):
    """Initialize model similarly to "All you need is a good init".

    References.
    ----------
    https://arxiv.org/abs/1511.06422
    """
    modules = get_modules(model, lambda layer: isinstance(layer, nn.Linear))
    x, _ = next(iter(dataloader))
    with torch.no_grad():
        for module in modules:
            print(lsuv_module(model, module, x))
    return model
