"""Example DataSet creation."""

import logging

import numpy as np
import sentencepiece as spm
import torch
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from torch.utils.data import Dataset

from toadstool.utils import parallel_run

log = logging.getLogger(__name__)


class SequenceDataset(Dataset):
    """A Dataset to take DataFrame with sequences to a PyTorch Dataset.

    Meant to handle just numericalization of the sequence column,
    and the label column.
    Support for additional tokenizers just needs to be added to init
    """

    def __init__(self, data, text_col, tokenizer, label_col=None, label_encoder=None, max_len=None):
        """
        Dataset utilizing tokenizer and label_encoder over a pandas DataFrame.

        Parameters
        ----------
        data: pandas.DataFrame
        text_col: str
            The column of `data` to treat as the sequences to tokenize and to return as X
        label_col: str
            The column of `data` to treat as the labels and to return as y.
        tokenizer: str |  spm.SentencePieceProcessor
            Either the pathname to a saved tokenizer or a sentencepiece tokenizer
        label_encoder: sklearn target transformer
            See: https://scikit-learn.org/stable/modules/preprocessing_targets.html#preprocessing-targets
            Expects a prefitted encoder. See: `fit_label_encoder`
        """
        if label_col is not None:
            self.data = data[[text_col, label_col]].copy(deep=True)
        else:
            self.data = data[[text_col]].copy(deep=True)
        self.text_col = text_col
        self.label_col = label_col
        self.label_encoder = label_encoder

        # numericalize text column
        self.tokenizer = tokenizer
        if isinstance(self.tokenizer, spm.SentencePieceProcessor):
            encode_func = self.tokenizer.encode_as_ids
            #  self.data[text_col] = self.data[text_col].map(self.tokenizer.encode_as_ids)
        else:
            encode_func = self.tokenizer
            #  self.data[text_col] = self.data[text_col].map(self.tokenizer)
        self.data[text_col] = parallel_run(encode_func, self.data[text_col])

        if max_len is not None:
            self.data[text_col] = self.data[text_col].map(lambda x: x[:max_len])

        # numericalize labels
        log.debug(f'label_col: {label_col} and label_encoder: {label_encoder}')
        if self.label_col is not None and self.label_encoder is None:
            raise Exception('No way to numericalize label_col without label_encoder')

        if self.label_col is not None:
            self.y = self.label_encoder.transform(self.data[self.label_col])

    def __len__(self):
        return self.data.shape[0]

    def __getitem__(self, idx):
        x = self.data[self.text_col].iloc[idx]
        if self.label_col is not None:
            y = self.y[idx]

            if isinstance(y, np.ndarray):
                y = torch.as_tensor(y).float()
            else:
                y = torch.as_tensor(y).long()
            return x, y
        return x

    def __repr__(self):
        return (
            f'{self.__class__.__name__}:'
            f'\n\tdata:  {self.data.shape}'
            f'\n\ttext:  {self.text_col}'
            f'\n\tlabel: {self.label_col}'
            f'\n\tvocab: {self.tokenizer.vocab_size()}'
        )


def fit_label_encoder(df, label):
    """Create a sklearn.preprocessing.LabelEncoder over the `label` column in `df`.

    Parameters
    ----------
    df: pandas.DataFrame
    label: str
        column name in `df`
    """
    encoder = LabelEncoder()
    encoder.fit(df[label])
    return encoder


def fit_label_binarizer(df, label):
    """Create a sklearn.preprocessing.OneHotEncoder over the `label` column in `df`.

    Parameters
    ----------
    df: pandas.DataFrame
    label: str
        column name in `df`
    """
    encoder = LabelBinarizer()
    encoder.fit(df[label])
    return encoder
