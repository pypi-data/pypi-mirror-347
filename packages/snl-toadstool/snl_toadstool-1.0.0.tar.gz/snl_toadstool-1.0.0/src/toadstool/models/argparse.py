"""Helper scripts to allow easy configuration of example models to popular architectures and cli parsing."""

import argparse
from functools import partial

from toadstool.utils import read_config

TRANSFORMER_PARAMS = {
    'BERT': {
        'emb_size': 768,
        'nhead': 12,
        'num_encoder_layers': 12,
        'num_decoder_layers': 0,
        'pos_max_len': 512,
        'dim_feedforward': 3072,  # 4*emb_size
    },
    'BERT_LARGE': {
        'emb_size': 1024,
        'nhead': 16,
        'num_encoder_layers': 24,
        'num_decoder_layers': 0,
        'pos_max_len': 512,
        'dim_feedforward': 4096,
    },
    'GPT2': {
        'emb_size': 768,
        'nhead': 12,
        'pos_embeddings': 'learned',
        'pos_max_len': 1024,
        'num_encoder_layers': 0,
        'num_decoder_layers': 12,
        'dim_feedforward': 3072,
    },
    'GPT2_XL': {
        'emb_size': 1600,
        'nhead': 25,
        'pos_embeddings': 'learned',
        'pos_max_len': 1024,
        'num_encoder_layers': 0,
        'num_decoder_layers': 48,
        'dim_feedforward': 3072,
    },
}

MIXER_PARAMS = {
    'BERT': {
        'emb_size': 768,
        #  'nhead': 12,
        'num_blocks': 12,
        'seq_len': 512,
        'token_dim': 3072,
        'channel_dim': 3072,
    },
    'BERT_LARGE': {
        'emb_size': 1024,
        #  'nhead': 16,
        'num_blocks': 24,
        'seq_len': 512,
        'token_dim': 4096,
        'channel_dim': 4096,
    },
}

SEQCONV_PARAMS = {
    'BERT': {
        'dim_embed': 768,
        'n_heads': 12,
        'n_enc_layers': 9,
        'n_dec_layers': 0,
        'n_encodings': 512,
        #'dim_feedforward': 3072 # 4*emb_size Not implemented in SeqConv yet
    }
}


class ModelArgs(argparse.Action):
    """This allows a default set of parameters to be set as well as selectively parsing
    any supplied commandline arguments, if they are specified like `--toadstool <key>:<value>,...,
    into a dictionary.
    """

    def __init__(self, std_params, *args, **kwargs):
        self.STD_PARAMS = std_params
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        d = {}
        default = parser.get_default(self.dest)
        if default is not None:
            if default in self.STD_PARAMS:
                default = self.STD_PARAMS[default]
            d.update(default)
        if isinstance(values, str) and values in self.STD_PARAMS:
            d.update(self.STD_PARAMS[values])
        elif isinstance(values, str):
            for item in values.split(','):
                key, value = item.split(':')
                d[key] = int(value) if value.isdigit() else value
        elif isinstance(values, dict):
            d.update(values)
        elif values:
            raise TypeError(f"Don't know how to handle type: {type(values)}")
        setattr(namespace, self.dest, d)


TransformerArgs = partial(ModelArgs, TRANSFORMER_PARAMS)
MixerArgs = partial(ModelArgs, MIXER_PARAMS)
SeqConvArgs = partial(ModelArgs, SEQCONV_PARAMS)


def argparse_config():
    """To try and parse a config file if supplied."""
    parser = argparse.ArgumentParser(description='Optionally load config file.', add_help=False)
    parser.add_argument('-c', '--config', type=str, help='Config file')
    args, remaining_args = parser.parse_known_args()
    if args.config is not None:
        return read_config(args.config), remaining_args
    return None, remaining_args


def args_to_config(args, ignore_values=None):
    """Parse argparse arguments into a dictionary of values that should differentiate this run
        For use in `PipelineDirStruct`.
    Used to write out a config file.
    """
    config = vars(args).copy()
    if ignore_values is None:
        ignore_values = []
    for val in ignore_values:
        if val in config:
            del config[val]
    return config
