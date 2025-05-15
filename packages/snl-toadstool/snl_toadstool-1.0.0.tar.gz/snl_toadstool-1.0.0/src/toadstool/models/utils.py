"""Helper functions for models."""

import warnings
from functools import partial

import torch
from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import (
    CheckpointImpl,
    apply_activation_checkpointing,
    checkpoint_wrapper,
)
from torch.distributed.fsdp import BackwardPrefetch, MixedPrecision, ShardingStrategy
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from torch.nn import TransformerDecoderLayer, TransformerEncoderLayer
from torch.nn.parallel import DistributedDataParallel as DDP

from toadstool.models.zoo.MLPMixer import MixerBlock

TOADSTOOL_MODEL_BLOCKS = {TransformerEncoderLayer, TransformerDecoderLayer, MixerBlock}

toadstool_default_autowrap_policy = partial(
    transformer_auto_wrap_policy,
    transformer_layer_cls=TOADSTOOL_MODEL_BLOCKS,
)

fp16_policy = MixedPrecision(
    param_dtype=torch.float16,
    # Gradient communication precision.
    reduce_dtype=torch.float16,
    # Buffer precision.
    buffer_dtype=torch.float16,
)
fp32_policy = MixedPrecision(
    param_dtype=torch.float32,
    reduce_dtype=torch.float32,
    buffer_dtype=torch.float32,
)
bfp16_policy = MixedPrecision(param_dtype=torch.bfloat16, reduce_dtype=torch.bfloat16, buffer_dtype=torch.bfloat16)


def fsdp_wrap(
    model,
    device,
    mp_policy=bfp16_policy,
    auto_wrap_policy=toadstool_default_autowrap_policy,
    sharding_strategy=ShardingStrategy.FULL_SHARD,
    backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
    cpu_offload=None,
):
    """Helper function to create a default FSDP model."""
    bf16_ready = (
        torch.version.cuda
        and torch.cuda.is_bf16_supported()
        #  and LooseVersion(torch.version.cuda) >= "11.0"
        and torch.distributed.is_nccl_available()
        and torch.cuda.nccl.version() >= (2, 10)
    )

    if not bf16_ready and mp_policy is bfp16_policy:
        warnings.warn(
            'bfloat16 not supported, switching from bfloat16 default policy for fp16_policy. Manually create policy if you want to force it'
        )
        mp_policy = fp16_policy

    torch.cuda.set_device(device)
    return FSDP(
        model.to(device),
        auto_wrap_policy=auto_wrap_policy,
        mixed_precision=mp_policy,
        sharding_strategy=sharding_strategy,
        backward_prefetch=backward_prefetch,
        cpu_offload=cpu_offload,
    )
    #  cpu_offload=CPUOffload(offload_params=True))


def fsdp_checkpoint(model, blocks=TOADSTOOL_MODEL_BLOCKS, checkpoint_impl=CheckpointImpl.NO_REENTRANT):
    non_reentrant_wrapper = partial(checkpoint_wrapper, checkpoint_impl=checkpoint_impl)
    apply_activation_checkpointing(
        model,
        checkpoint_wrapper_fn=non_reentrant_wrapper,
        check_fn=lambda submodule: isinstance(submodule, tuple(blocks)),
    )


def ddp_wrap(model, device):
    """Helper function to create a default DDP model."""
    return DDP(model.to(device), find_unused_parameters=True, device_ids=[device])


def summarize_model(model):
    """Print out number of parameters of a model."""
    num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f'Model # of parameters: {num_params:,}')
    return num_params


def gen_padding_mask(max_len, x_lens):
    """Generate a PyTorch bool Tensor False(0)-Not Padding, True(1)-Padding.

    Parameters
    ----------
    max_len: int
        size of the mask
    x_lens: list[int]
        list of sizes to be masked to

    Returns
    -------
    mask: torch.BoolTensor
    """
    entire_mask = torch.zeros(x_lens.shape[0], max_len)
    for i, length in enumerate(x_lens):
        mask = torch.cat((torch.zeros(length), torch.ones(max_len - length)))
        entire_mask[i] = mask

    return entire_mask.bool()


class Hook:
    def __init__(self, module, func):
        self.hook = module.register_forward_hook(partial(func, self))
        self.encodings = []

    def remove(self):
        self.hook.remove()

    def __del__(self):
        self.remove()
