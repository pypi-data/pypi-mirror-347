"""Mlp-mixer inspired model for sequence classification.

@article{tolstikhin2021mlp,
  title={Mlp-mixer: An all-mlp architecture for vision},
  author={Tolstikhin, Ilya O and Houlsby, Neil and Kolesnikov, Alexander and Beyer, Lucas and Zhai, Xiaohua and Unterthiner, Thomas and Yung, Jessica and Steiner, Andreas and Keysers, Daniel and Uszkoreit, Jakob and others},
  journal={Advances in neural information processing systems},
  volume={34},
  pages={24261--24272},
  year={2021}
}"""

import torch
import torch.nn.functional as F
from torch import nn


class MlpMixer(nn.Module):
    def __init__(self, vocab_size, num_blocks, seq_len, emb_size, token_dim, channel_dim, pad_id, num_classes=None):
        """
        Parameters
        ----------
        vocab_size
        num_blocks
        seq_len
        emb_size
        token_dim: int
            hidden dimension for the token mixer
        channel_dim: int
            hidden dimension for the channel mixer
        pad_id
        num_classes
        """
        super().__init__()
        self.pad_id = pad_id
        self.seq_len = seq_len
        self.embed = nn.Embedding(vocab_size, emb_size, padding_idx=pad_id)

        mixing = []
        for _ in range(num_blocks):
            mixing.append(MixerBlock(seq_len, emb_size, token_dim, channel_dim))
        self.mixing = nn.Sequential(*mixing)

        self.norm = nn.LayerNorm(emb_size)
        self.proj_bias = nn.Parameter(torch.zeros(vocab_size))

        self.classifier = None
        if num_classes is not None:
            self.classifier = nn.Linear(emb_size, num_classes)

    def forward(self, inp):
        if isinstance(inp, dict):
            x = inp['src']
            tgt = inp.get('tgt', None)
            mask = inp.get('mask', None)
            if mask is not None:
                mask = torch.nn.functional.pad(mask, (0, self.seq_len - mask.shape[1]), value=0)
        else:
            x = inp
            tgt = None  # noqa F841
            mask = None
        x = torch.nn.functional.pad(x, (0, self.seq_len - x.shape[1]), value=self.pad_id)
        x = self.embed(x)
        x = self.mixing(x)

        x = self.norm(x)
        x = self.out(x)
        if mask is not None:
            x = x[mask]
        return x

    def out(self, out):
        if self.classifier is None:
            return F.linear(out, self.embed.weight, self.proj_bias)
        return self.classifier(out.mean(dim=1))


class MixerBlock(nn.Module):
    def __init__(self, seq_len, emb_size, token_dim, channel_dim):
        super().__init__()
        self.token_norm = nn.LayerNorm(emb_size)
        self.token_mix = MlpBlock(seq_len, token_dim)
        self.channel_norm = nn.LayerNorm(emb_size)
        self.channel_mix = MlpBlock(emb_size, channel_dim)

    def forward(self, x):
        x_p = self.token_norm(x)
        x_p = torch.permute(x_p, (0, 2, 1))
        x_p = self.token_mix(x_p)
        x_p = torch.permute(x_p, (0, 2, 1))
        x = x + x_p
        x_p = self.channel_norm(x)
        return x + self.channel_mix(x_p)


class MlpBlock(nn.Module):
    def __init__(self, in_dim, hidden_dim):
        super().__init__()
        self.in_layer = nn.Linear(in_dim, hidden_dim)
        self.out_layer = nn.Linear(hidden_dim, in_dim)

    def forward(self, x):
        x = nn.functional.gelu(self.in_layer(x))
        return self.out_layer(x)
