"""Code to collate for DataLoaders."""

import torch

from .mlm import bert

__all__ = ['bert', 'pad_truncate']


def pad_truncate(batch, pad_id, max_length=1024):
    """To pad uneven list of tensors together."""
    just_x = False
    if isinstance(batch[0], tuple):
        x, y = zip(*batch)
    else:
        just_x = True
        x, y = batch, []
    x = [torch.LongTensor(x)[:max_length] for x in x]
    x = torch.nn.utils.rnn.pad_sequence(x, batch_first=True, padding_value=pad_id)
    x = torch.LongTensor(x)
    if just_x:
        return x
    return x, torch.stack(y)
