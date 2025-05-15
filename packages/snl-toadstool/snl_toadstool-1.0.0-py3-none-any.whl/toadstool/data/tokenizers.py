"""Example tokenizers to utilize with toadstool.data.datasets.SequenceDataset."""

import itertools
import re
from pathlib import Path

import numpy as np
import pandas as pd
import sentencepiece as spm

UNKNOWN_TOKEN = 'unk'  # noqa S105


class ByteTokenizer:
    """Raw byte tokenizer."""

    def __init__(self, special_ids=None):
        self.special_ids = special_ids if special_ids is not None else []
        if '<pad>' not in self.special_ids:
            self.special_ids.append('<pad>')
        if '<eos>' not in self.special_ids:
            self.special_ids.append('<eos>')

    def __call__(self, inp):
        if isinstance(inp, str):
            return [x + len(self.special_ids) for x in inp.encode('utf-8')]
        return self.transform(inp)

    def transform(self, sentences):
        if isinstance(sentences, pd.Series):
            return sentences.apply(self)
        return [self(s) for s in sentences]

    def vocab_size(self):
        return 256 + len(self.special_ids)

    def pad_id(self):
        return self.special_ids.index('<pad>')


class BoringTokenizer:
    """A boring tokenizer."""

    def __init__(self, tokenize_func, vocab=None):
        """Create a generic tokenizer based on passed `tokenize_func`.

        Parameters
        ----------
        tokenize_func: str | Callable[str]
            The tokenization function to use, should accept a string and return a list of tokens.
            If is a string, will lookup in our predefined table for the corresponding functions.
        vocab: pandas.Index
            Numericalization happens with look ups into this.
            See: `get_vocab`
        """
        if isinstance(tokenize_func, str):
            tokenizer_map = {
                'seq': quote_tokenizer,
            }
            tokenize_func = tokenizer_map[tokenize_func]
        self.vocab = vocab
        self.tokenizer = tokenize_func

    def __call__(self, inp):
        if isinstance(inp, str):
            return self.token_and_numericalize(inp)
        return self.transform(inp)

    def fit(self, sentences, min_count=10, max_vocab=10000):
        self.vocab = get_vocab(sentences, self.tokenizer, min_count, max_vocab)

    def transform(self, sentences):
        if isinstance(sentences, pd.Series):
            return sentences.apply(self.token_and_numericalize)
        return [self.token_and_numericalize(s) for s in sentences]

    def token_and_numericalize(self, seq):
        # Tokenize and numericalize in one pass
        return list(self._numericalize(self.tokenizer(seq)))

    def _numericalize(self, tokens):
        """
        Turns a list of tokens to a list of indices corresponding to the vocab.

        Parameters
        ----------
            tokens: list
            vocab: pandas.Index
        """
        for token in tokens:
            if token in self.vocab:
                yield self.vocab.get_loc(token)
            else:
                yield self.vocab.get_loc(UNKNOWN_TOKEN)

    def vocab_size(self):
        return len(self.vocab) + 1  # pad_id

    def pad_id(self):
        return len(self.vocab)


def get_vocab(sentences, tokenizer, min_count=None, max_vocab=None, add_unknown=True):
    """Creates an ordered Index of tokens to use as a vocabulary.

    Appends `UNKNOWN_TOKEN` as a token for use in `numericalize(tokens, vocab)` when numericalizing a new set of tokens.

    Parameters
    ----------
        sentences: list<string>
            list of strings of all the "sentences" which will be concatted, tokenized, and counted
        tokenizer: function
            function to take the concatted version of all the text and convert to a list of tokens
        min_count: int
            a token must be used > `min_count` times to be included in the vocabulary
        max_vocab: int
            maximum number of tokens to include in the vocabulary

    Returns
    -------
        vocab: pandas.Index
            vocabulary
    """
    words = itertools.chain(*[tokenizer(x) for x in sentences])
    vocab = pd.Series(words).value_counts()
    vocab = vocab.iloc[np.lexsort((vocab.index, -vocab.to_numpy()))]
    if min_count is not None:
        vocab = vocab[vocab > min_count]
    if max_vocab is not None:
        vocab = vocab[:max_vocab]
    vocab = vocab.index  # .sort_values()
    if add_unknown:
        vocab = vocab.append(pd.Index([UNKNOWN_TOKEN]))
    return vocab


def bytes_tokenizer(sentence, word_size=1):
    """
    Parameters
    ----------
        word_size: int
            number of bytes to consider a word

    Notes
    -----
        2-hex values == '..' == 1 byte.
    """
    return re.findall('..' * word_size, sentence)


def quote_tokenizer(sentence, split_all_words=True):
    """
    For outputs `"<word> <word>*" "<word> <word>*"...'
    `split_all_words` decides whether we split on ' ' (if True) or '" "'.
    It also removes all " in the tokens.

    Parameters
    ----------
        split_all_words: boolean
            If each word of quoted strings should be considered a separate word
    """
    if split_all_words:
        return re.sub('"', '', sentence).strip().split(' ')
    return [re.sub('"', '', word.strip()) for word in sentence.strip().split('" "')]


def train_spm_tokenizer(
    input_fn, model_prefix, model_type='bpe', pad_id=3, pad_piece='[PAD]', user_defined_symbols='', vocab_size=10000
):
    assert Path(input_fn).exists()
    spm.SentencePieceTrainer.train(
        model_prefix=model_prefix,
        input=input_fn,
        vocab_size=vocab_size,
        character_coverage=1.0,
        model_type=model_type,
        pad_id=pad_id,
        pad_piece=pad_piece,
        user_defined_symbols=user_defined_symbols,
    )
    return f'{model_prefix}.model'


def load_spm_tokenizer(model_file):
    return spm.SentencePieceProcessor(model_file=str(model_file))


def train_boring_tokenizer(df, seq_col, min_count=10, max_vocab=10000):
    tokenizer = BoringTokenizer(seq_col)
    tokenizer.fit(df[seq_col], min_count, max_vocab)
    return tokenizer
