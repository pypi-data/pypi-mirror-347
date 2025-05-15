from pathlib import Path
import tempfile

from toadstool import utils


def test_filter_instance_returns_filter_for_objects_of_type():
    lst = [1, '2', 3, '4', 5]
    assert isinstance(utils.filter_instance(str, lst), filter)


def test_filter_instance_filters_as_expected():
    lst = [1, '2', 3, '4', 5]
    filtered = list(utils.filter_instance(str, lst))
    assert filtered == ['2', '4']


def test_walkdir_with_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        rootfile = tmpdir / 'file1'
        subdir = tmpdir / 'subdir'
        subfile = subdir / 'file2'

        subdir.mkdir(parents=True)
        rootfile.touch()
        subfile.touch()
        paths = utils.walkdir_with_path(tmpdir)
        for p in paths:
            assert p in [rootfile, subfile]


def test_parallel_run_returns_list_of_correct_results():
    func = sum
    seq = [[1, 2, 3, 4], [5, 6, 7, 8], [1, 3, 5, 7]]
    nprocs = 1
    assert utils.parallel_run(func, seq, nprocs=nprocs) == [10, 26, 16]
