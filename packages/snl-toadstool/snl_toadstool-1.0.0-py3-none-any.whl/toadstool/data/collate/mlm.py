"""Code for carrying out masked-language modeling."""

import warnings

import torch


def bert(batch, mlm_prob, vocab_size, bos_id, mask_id, pad_id, no_mask_ids=None, huggingFace=False):
    """BERT style mlm.

    Parameters
    ----------
    batch: Tensor
        Samples to perform masking on

    mlm_prob: float
        Probability of masking a token during training

    vocab_size: int
        Size of vocabulary

    bos_id: int
        Value for beginning of sequence token

    mask_id: int
        Value for mask token

    pad_id: int
        Value of padding token

    no_mask_ids: List[int]
        ids to avoid masking

    huggingFace: bool
        Whether to use HuggingFace framework masking or not

    Returns
    -------
    dict
        src, target, and mask dict

    torch.Tensor
        Labels
    """
    try:
        assert bos_id >= vocab_size
        assert pad_id >= vocab_size
        assert mask_id >= vocab_size
        for i in no_mask_ids:
            assert i >= vocab_size
    except AssertionError:
        warnings.warn('id to not mask < vocab_size, so may be randomly replaced')
    if no_mask_ids is None:
        no_mask_ids = []
    batch = [torch.as_tensor(x) for x in batch]

    src = torch.nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=pad_id)
    orig = src.clone()
    tgt = torch.cat(
        (torch.full((orig.shape[0], 1), bos_id).long(), orig[:, :-1]), dim=1
    )  # Transformer tgt should be shifted by 1

    mask_prob_matrix = torch.full(src.shape, mlm_prob)

    # Don't mask the pad id or other special ids
    dont_mask = torch.zeros(orig.shape).bool()
    for tok_id in [bos_id, pad_id, mask_id, *no_mask_ids]:
        dont_mask[src == tok_id] = 1
    mask_prob_matrix.masked_fill_(dont_mask, 0)
    mask = torch.bernoulli(mask_prob_matrix).bool()
    y = orig[mask]

    # BERT masking
    # If the i-th token is chosen, we replace the i-th token with
    # (1) the [MASK] token 80% of the time
    mask_replace = torch.bernoulli(torch.full(orig.shape, 0.8)).bool() & mask
    src[mask_replace] = mask_id
    # (2) a random token 10% of the time
    random_replace = torch.bernoulli(torch.full(orig.shape, 0.1)).bool() & mask & ~mask_replace
    src[random_replace] = torch.randint(vocab_size, src.shape, dtype=torch.long)[random_replace]
    # (3) the unchanged i-th token 10% of the time.

    if huggingFace:
        tgt[~mask] = -100
        return {'input_ids': src, 'labels': tgt}
    return {'src': src, 'tgt': tgt, 'mask': mask}, y.flatten()
