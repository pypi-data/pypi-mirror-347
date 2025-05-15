"""Evaluations based on margin (difference between highest and next highest scores)."""

import warnings

import numpy as np
import sklearn
import torch
from tqdm.auto import tqdm


def margin_precision_recall_curve(target, logits):
    """Create a precision recall curve, based on margin of predictions."""
    if target.ndim == 1:
        probs = torch.nn.functional.softmax(logits, dim=1)
        y = target
    else:
        probs = torch.sigmoid(logits)

        warnings.warn("Multi-label isn't supported so just taking 1 class per instance")
        y = target[:, 26].long()

    y_p = probs[:, 26]  # logits.max(1)[1]

    margin = calc_margin(probs)
    thresholds = np.unique(margin)
    thresholds = thresholds[thresholds.argsort()]

    pr = []
    for t in tqdm(thresholds):
        pr.append(calc_pr_helper(t, margin, y, y_p))

    return *zip(*pr), thresholds


def calc_pr_helper(t, margin, y, y_p):
    above = margin > t
    cury, cury_p = y[above], y_p[above] > 0.5

    p = sklearn.metrics.precision_score(cury, cury_p, average='binary', zero_division=0)
    r = sklearn.metrics.recall_score(cury, cury_p, average='binary', zero_division=0)
    return p, r


def calc_margin(probs):
    """Given probabilities calculate the margin (difference between highest and next highest probability)."""
    v, _ = probs.topk(2)
    return torch.abs(v[:, 0] - v[:, 1])
