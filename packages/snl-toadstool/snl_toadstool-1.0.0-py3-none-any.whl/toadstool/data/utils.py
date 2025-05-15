"""Helper functions for handling DL data."""

import functools
import logging
import math
import warnings
from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.model_selection import GroupShuffleSplit, KFold, StratifiedKFold, train_test_split
from torch.utils.data import DataLoader, Subset
from torch.utils.data.distributed import DistributedSampler

log = logging.getLogger(__name__)


def print_corr(corr):
    """Print an already computed correlation matrix."""
    f = plt.figure(figsize=(40, 20))
    plt.matshow(corr, fignum=f.number, vmin=-1, vmax=1)
    plt.xticks(range(len(corr.columns)), corr.columns, fontsize=14, rotation=90)
    plt.yticks(range(len(corr.index)), corr.index, fontsize=14)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)


def split_indices(dataset, train_ratio=0.8, test_ratio=0.1, stratify=None, seed=0):
    """Given a dataset (really anything that can be called with `len(dataset)`)
        return 3 list of indices that partition it into train, valid, and test sets
        based on the provided ratios, optionally respecting `stratify`.

    See Also: `group_train_test_valid_split`
    """
    size = len(dataset)

    torch.manual_seed(seed)

    train_idxs = range(size)
    test_idxs = []
    valid_idxs = []
    # Split into train test
    if train_ratio >= 1:
        warnings.warn('Everything going into training')
        rng = np.random.default_rng()
        return rng.permutation(train_idxs), [], []
    if test_ratio >= 1:
        warnings.warn('Everything going into testing')
        rng = np.random.default_rng()
        return [], [], rng.permutation(train_idxs)

    train_idxs, test_idxs = train_test_split(range(size), train_size=train_ratio, stratify=stratify, random_state=seed)
    # Split test to test valid if necessary
    if train_ratio + test_ratio < 1:
        if test_ratio == 0:
            valid_idxs, test_idxs = test_idxs, valid_idxs
        else:
            test_strat = None if stratify is None else np.array(stratify)[test_idxs]
            test_idxs, valid_idxs = train_test_split(
                test_idxs, train_size=test_ratio / (1 - train_ratio), stratify=test_strat, random_state=seed
            )

    return train_idxs, valid_idxs, test_idxs


class SplitDataset:
    """Create an object that holds train, valid, and test datasets, based on an already existing dataset. And create corresponding dataloaders.

    Utilizes `split_indices`, `to_dataloaders`, and PyTorch's `Subset`.
    `.train`, `.valid`, `.test` - Subsetted DataSets
    `.trainl`, `.validl`, `.testl` - Corresponding DataLoaders
    """

    def __init__(
        self, dataset, train_ratio=0.8, test_ratio=0.1, seed=0, stratify=None, isDistributed=False, **DataLoader_kwargs
    ):
        """
        Will error with train_ratio == 1 and stratify != None due to train_test_split.

        Parameters
        ----------
            dataset: torch.data.Dataset
                Dataset to split and wrap in DataLoaders
            train_ratio: float <= 1
                percent of data to use as training data. 1-(train_ratio+test_ratio) will be used for validation data.
            test_ratio: float <= 1
                percent of data to use as testing data. 1-(train_ratio+test_ratio) will be used for validation data.
            seed: int
                random seed to use for reproducability
            stratify: list
                stratification of the data
            isDistributed: boolean
                whether to use the DistributedSampler
            DataLoader_kwargs: dict
                arguments to be passed to torch.data.DataLoader
        """
        train_idxs, valid_idxs, test_idxs = split_indices(dataset, train_ratio, test_ratio, stratify, seed)

        self.train = Subset(dataset, train_idxs)
        self.valid = Subset(dataset, valid_idxs)
        self.test = Subset(dataset, test_idxs)

        self.trainl, self.validl, self.testl = to_dataloaders(
            self.train, self.valid, self.test, isDistributed, **DataLoader_kwargs
        )

    def __repr__(self):
        return f'{self.__class__.__name__} train:{len(self.train)} valid:{len(self.valid)} test:{len(self.test)}'


def to_dataloaders(train, valid, test, isDistributed=False, **DataLoader_kwargs):
    """Convenience function to convert 3 Datasets to DataLoaders
    See: `to_dataloader`.
    """
    trainl = to_dataloader(train, isDistributed, isTrain=True, **DataLoader_kwargs)
    validl = to_dataloader(valid, isDistributed, **DataLoader_kwargs)
    testl = to_dataloader(test, isDistributed, **DataLoader_kwargs)
    return trainl, validl, testl


def to_dataloader(dataset, isDistributed=False, isTrain=False, **DataLoader_kwargs):
    """Create a DataLoader based on the dataset, slightly intelligently.

    Parameters
    ----------
    dataset: torch.utils.data.DataSet
    isDistributed: bool
        Controls whether it adds the DistributedSampler
    isTrain: bool
        Tries to insure we are shuffling if True
    **kwargs:
        All other parameters are passed directly to the DataLoader call
    """
    if isDistributed and DataLoader_kwargs.get('num_workers', 1) > 1:
        warnings.warn('num_workers > 1 for distributed training')
    if isDistributed:
        if DataLoader_kwargs.get('sampler'):
            log.error('Provided sampler on distributed dataloader.')
        return DataLoader(dataset, sampler=DistributedSampler(dataset), **DataLoader_kwargs)
    if isTrain:
        sampler = DataLoader_kwargs.get('sampler')
        shuffle = DataLoader_kwargs.get('shuffle')
        if sampler is None and shuffle is None:
            log.warning('Setting shuffle=True on train dataset')
            return DataLoader(dataset, shuffle=True, **DataLoader_kwargs)
    return DataLoader(dataset, **DataLoader_kwargs)


def kfold_dataset(
    dataset, seed=0, batch_size=32, num_workers=16, pin_memory=False, kfolds=5, strat_labels=None, preshuffle=True
):
    """Split a dataset into k-fold subsets. Each Fold has `.train` `.valid` `.trainl` and `.validl`
        For accessing the Fold's corresponding DataSets and DataLoaders respectively.
    run should be an "experiment" (i.e. function) that accepts (name, train, test, **kwargs).
    """
    if strat_labels is None:
        folder = KFold(n_splits=kfolds, shuffle=preshuffle, random_state=seed)
        folds = folder.split(dataset)
    else:
        folder = StratifiedKFold(n_splits=kfolds, shuffle=preshuffle, random_state=seed)
        folds = folder.split(dataset, strat_labels)

    Fold = namedtuple('Fold', ['train', 'valid', 'trainl', 'validl'])

    for train_idx, valid_idx in folds:
        train = torch.utils.data.Subset(dataset, train_idx)
        valid = torch.utils.data.Subset(dataset, valid_idx)

        loader_func = functools.partial(
            DataLoader, batch_size=batch_size, num_workers=num_workers, pin_memory=pin_memory
        )

        trainl = loader_func(train, shuffle=True)
        validl = loader_func(valid)

        yield Fold(train, valid, trainl, validl)


def standardize(x, mean=None, std=None):
    """(x-mean)/std, but slightly more intelligently."""
    # std[std==0] = 1
    #    sklearn's StandardScaler basically does this, but I think it would be better to just ignore the column so I do the replace below.
    if mean is None or std is None:
        assert mean is std
    if mean is None:
        mean = x.mean()
    if std is None:
        std = x.std()

    return ((x - mean) / std).fillna(0).replace([np.inf, -np.inf], 0)


def calc_batch_size(num_params, max_instance_size):
    """Heuristic to try and determine the max batch size the GPU can handle."""
    model_bytes = num_params * 4
    instance_bytes = max_instance_size * 4

    t = torch.cuda.get_device_properties(0).total_memory

    batch_size = (t - model_bytes) / (8 * num_params + instance_bytes)
    # batch_size = math.floor((t - model_bytes)/instance_bytes)
    return int(batch_size), int(math.pow(2, math.floor(math.log(batch_size) / math.log(2))))


def group_train_test_valid_split(df, split_col):
    """Get list of indices for train/valid/test splits for a given dataframe, stratified based on `split_col`."""
    # If we don't have strat values we at least get 1 for each train and test set otherwise 20%
    total_groups = len(df[split_col].value_counts())
    split = 2 if total_groups < 10 else 0.2

    train_splitter = GroupShuffleSplit(n_splits=1, test_size=split, random_state=0)
    train_idxs, valid_test_idxs = next(train_splitter.split(df, groups=df[split_col]))
    v_df = df.iloc[valid_test_idxs]

    # split the valid and test sets equally
    test_splitter = GroupShuffleSplit(n_splits=1, train_size=0.5, random_state=0)
    valid_idxs, test_idxs = next(test_splitter.split(v_df, groups=v_df[split_col]))
    valid_idxs = valid_test_idxs[valid_idxs]
    test_idxs = valid_test_idxs[test_idxs]
    return train_idxs, valid_idxs, test_idxs


def virtual_index(obj_lengths, idx):
    """If you have a list of objects you want to pretend are concatenated together,
    This will convert the concatenated index into the indices of which object and
    where in the object you need to index.
    """
    for obj_idx, obj_len in enumerate(obj_lengths):
        if idx < obj_len:
            return obj_idx, idx
        idx -= obj_len
    raise ValueError('Index too large for supplied list of object lengths')
