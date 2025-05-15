"""Code to support running in distributed or DistributedDataParallel manner. See the examples folder."""

import os
import warnings
from functools import partial

import torch
import torch.distributed as dist
import torch.multiprocessing as mp

# DataParallel(model, device_ids=list(range(torch.cuda.device_count())))


def setup_torch(proc_id, node_id, world_description, run_fn):
    """Setup torch.distributed default process group.

    Parameters
    ----------
    proc_id: int
        Process number spawned on this node.
        Used to calculate which rank we are.
        Typically which GPU index we should run on.
    node_id: int
        Which node we are running on.
        Used to calculate which rank we are.
    world_description: List[int]
        List of processes per node that should be running.
        Used to calculate world size and rank.
    run_fn: Callable[[rank: int, device: int], void]
        Function to run.
    """
    rank = sum(world_description[:node_id]) + proc_id
    world_size = sum(world_description)
    # print(f'rank:{rank} gpu_id:{proc_id} node_id:{node_id} world_size:{world_size}')

    # Using a shared file for communication instead
    # dist.init_process_group("nccl", init_method='file://<sharedfile_path>', rank=rank, world_size=world_size)
    dist.init_process_group('nccl', init_method='env://', rank=rank, world_size=world_size)

    run_fn(rank=rank, device=proc_id)

    dist.destroy_process_group()


def setup_deepspeed(proc_id, node_id, world_description, run_fn):
    """
    Setup deepspeed distributed
    See: setup_torch.
    """
    import deepspeed  # Don't want to depend on this if we aren't using it

    rank = sum(world_description[:node_id]) + proc_id
    world_size = sum(world_description)

    os.environ['LOCAL_RANK'] = str(proc_id)
    os.environ['RANK'] = str(rank)
    os.environ['WORLD_SIZE'] = str(world_size)
    deepspeed.init_distributed(dist_backend='nccl', init_method='env://', auto_mpi_discovery=False)
    run_fn(rank=rank, device=proc_id)


def slurm_run(run_fn, **kwargs):
    """
    Helper function to setup based on common SLURM env variables.
    This doesn't specify world_description which is an implicit assertion that we have the same number of gpus on each node.
    """
    first_nodelist = os.environ['SLURM_JOB_NODELIST'].split(',')[0]
    if '[' in first_nodelist:
        a = first_nodelist.split('[')
        first_node = a[0] + a[1].split('-')[0]
    else:
        first_node = first_nodelist

    manual_run(
        run_fn, first_node, 12234, int(os.environ['SLURM_NODEID']), int(os.environ['SLURM_JOB_NUM_NODES']), **kwargs
    )
    #  manual_run(run_fn, os.environ['SLURM_SUBMIT_HOST'], 12234, int(os.environ['SLURM_NODEID']), int(os.environ['SLURM_JOB_NUM_NODES']))


def single_node_run(run_fn, **kwargs):
    """Helper function to setup based multiple GPUs on a single node.
    Should be faster than normal DataParallel.
    """
    manual_run(run_fn, '127.0.0.1', 12235, 0, 1, **kwargs)


def manual_run(
    run_fn,
    master_addr,
    master_port,
    node_id,
    num_nodes,
    num_gpus='all',
    world_description='identical',
    setup=setup_torch,
    **kwargs,
):
    """
    Run the `run_fn` on all processes.
    Conceptually term 'gpu' and 'process' could be interchangeable if that helps understanding, but as the designed use case is for
        utilizing multiple 'gpu's that term is used here.

    Parameters
    ----------
    run_fn: func(rank:int, proc_id:int)
        Function for all processes to execute, that accepts rank and proc_id parameters
            (take into account they are all running the code and synchronization happens manually or through PyTorch's built in sync points)
    master_addr: str
        Address (e.g., "127.0.0.1") of the "master" address that provides coordination
    master_port: int/str
        Port number to connect to
    node_id: int
        What node (computer) is this running on.
    num_nodes: int
        How many nodes (computer) are running total
    num_gpus: int or 'all'
        How many duplicate processes to run for this node.
            e.g., Only data parallelism == 'all'
                  For model parallelism, only specify how many many copies of the model you'll have across the GPUs.
                      Placing the models on the correct GPUs is the responsibility of `run_fn`.
    world_description: 'identical' or List[int]
        Required if `num_gpus` is not the same on all nodes.
        Used to calculate the world_size and the process' rank.
    setup: func
        The setup function to initialize the distributed process group.
    kwargs: kwargs
        Any additional parameters to pass to the run_fn when spawning.
    """
    os.environ['MASTER_ADDR'] = master_addr
    os.environ['MASTER_PORT'] = str(master_port)
    num_gpus = torch.cuda.device_count() if num_gpus == 'all' else num_gpus

    if num_gpus > torch.cuda.device_count():
        warnings.warn('Spawning more processes than GPU resources')

    if world_description == 'identical':
        world_description = [num_gpus] * num_nodes
    assert len(world_description) == num_nodes, 'world_description is incomplete'
    assert isinstance(world_description, list)
    for i in world_description:
        assert isinstance(i, int)
    assert num_gpus == world_description[node_id], (
        "Current node's `num_gpu`'s is different than the `world_description`"
    )

    mp.spawn(setup, args=(node_id, world_description, partial(run_fn, **kwargs)), nprocs=num_gpus, join=True)
