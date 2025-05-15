"""Helper functions not specific to deep learning necessarily."""

import contextlib
import hashlib
import json
import os
import pathlib
import warnings
from itertools import zip_longest
from pathlib import Path

import torch.multiprocessing as mp
from tqdm.auto import tqdm


def filter_instance(obj, lst):
    """Get instance of obj in lst."""
    return filter(lambda x: isinstance(x, obj), lst)


def walkdir_with_path(folder):
    """Get generator of full path of all files in folder including subdirs."""
    for root, _, files in os.walk(folder):
        for file in files:
            yield Path(root) / file


def pprint_list(line):
    """Print a list with a little nicer format (pretty_print)."""
    for i in range(len(line))[::3]:
        for j in range(3):
            if i + j >= len(line):
                break
            print(f'{line[i + j]:30} ', end='')
        print('')


def side_by_side(f, s, width=80):
    """Print two strings vertically side by side."""
    for line, line_2 in zip_longest(f, s):
        if line is None:
            line = ''
        if line_2 is None:
            line_2 = ''
        if len(line) > width:
            line = line[: width - 3] + '...'
        if len(line_2) > width:
            line_2 = line_2[: width - 3] + '...'
        print(f'{line:{width}} | {line_2}')


def newer_deps(target, dependencies):
    """
    target: pathlib.Path,
    dependencies: List<Path|str>.

    check if any file in `dependencies` is newer than `target`
    """
    if not isinstance(target, pathlib.PurePath):
        target = pathlib.Path(target)
    if isinstance(dependencies, os.PathLike | str):
        warnings.warn("Doesn't look like you passed in an iterable thing. Trying to convert")
        dependencies = [dependencies]
    if not target.exists():
        return True
    mod_time = target.stat().st_mtime
    for dep in dependencies:
        if not isinstance(dep, pathlib.PurePath):
            dep = pathlib.Path(dep)
        if dep.stat().st_mtime > mod_time:
            return True
    return False


def parallel_run(func, seq, total=None, nprocs='auto', chunksize=100, context=None):
    """
    Convenience function to map `func` over `seq`.

    Parameters
    ----------
    func: function
        Function to run for each instance of seq as argument
    seq: iterable
        List or iterable to send each element as argument to function.
    total: int | None
        length of sequence or None it will try to call len(seq)
    nprocs: 'auto' | int
        if 'auto' will be os.sched_getaffinity, else how many processes to use
    chunksize: int
        size of each chunk seq is split by
    context: str | multiprocessing.Context
        if a custom context is needed

    Returns
    -------
    imap: iterator
        returns the iterator from pimap
    """
    if context is None:
        context = mp.get_context()
    elif isinstance(context, str):
        context = mp.get_context(context)

    if nprocs == 'auto':
        if hasattr(os, 'sched_getaffinity'):
            nprocs = len(os.sched_getaffinity(0))
        else:
            nprocs = os.cpu_count()
    if total is None:
        with contextlib.suppress(TypeError):
            total = len(seq)
    with context.Pool(processes=nprocs) as p:
        return list(tqdm(p.imap(func, seq, chunksize=chunksize), total=total))


def hash_dict(d):
    h = hashlib.sha256()
    h.update(json.dumps(d, sort_keys=True).encode())
    return h.hexdigest()


def read_config(fn):
    """Helper function just to make other code cleaner."""
    fn = Path(fn)
    return json.loads(fn.read_text())


def write_config(config, fn):
    """Want the writing config to be somewhat consistent."""
    fn = Path(fn)
    fn.parent.mkdir(parents=True, exist_ok=True)
    fn.write_text(json.dumps(config, sort_keys=True, indent=2))
