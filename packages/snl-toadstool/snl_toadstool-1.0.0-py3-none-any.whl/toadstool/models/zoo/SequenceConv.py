"""A convolutional based sequence model."""

from functools import partial

import torch.nn.functional as F
from torch import nn


class SequenceConv(nn.Module):
    def __init__(
        self,
        dim_in_vocab,
        dim_out_vocab=None,
        dim_embed=512,
        padding_idx=None,
        n_enc_layers=9,
        n_dec_layers=9,
        n_encodings=1,
        kernel_size=3,
        n_heads=1,
        stride=1,
    ):
        super().__init__()
        self.tok_embed = nn.Embedding(dim_in_vocab, dim_embed, padding_idx=padding_idx)

        encodeBlock = partial(
            GatedBlock,
            dim_embed=dim_embed,
            dim_kernel=kernel_size,
            encoder=True,
        )
        decodeBlock = partial(GatedBlock, dim_embed=dim_embed, dim_kernel=kernel_size, encoder=False)

        self.encoder = nn.ModuleList([encodeBlock(dilation=2**1) for i in range(n_enc_layers)])
        self.decoder = nn.ModuleList([decodeBlock(dilation=2**1) for i in range(n_dec_layers)])

        self.n_encodings = n_encodings
        self.pool = nn.AdaptiveMaxPool1d(n_encodings)

        if dim_out_vocab:
            self.lm_head = nn.Linear(dim_embed, dim_out_vocab)
        else:
            self.lm_head = nn.Linear(dim_embed, dim_in_vocab)
            self.lm_head.weight = self.tok_embed.weight

    def forward(self, x, targets=None):
        mask = None
        if isinstance(x, list):
            x, targets = x
        elif isinstance(x, dict):
            mask = x.get('mask', None)  # noqa F841
            targets = x.get('tgt', None)
            x = x.get('src')
        x = self.tok_embed(x)

        x = x.transpose(-2, -1)  # Because that's how convs like it (b, e, s)

        shrink_size = (x.size(2) - self.n_encodings) // len(self.encoder)
        for enc_layer in self.encoder:
            x = enc_layer(x, output_size=x.size(2) - shrink_size)

        x = self.pool(x)

        for dec_layer in self.decoder:
            x = dec_layer(x)
        if targets is not None:
            x = F.adaptive_avg_pool1d(x, targets.shape[1])
        x = x.transpose(-2, -1)  # (batch, seq_len, embed)
        return self.lm_head(x)


class ConvLayerNorm(nn.Module):
    def __init__(self, dim_embed):
        super().__init__()
        self.norm = nn.LayerNorm(dim_embed)

    def forward(self, x):
        x = x.transpose(-2, -1)  # b, e, s -> b, s, e
        x = self.norm(x)
        return x.transpose(-2, -1)  # b, s, e -> b, e, s


class GatedBlock(nn.Module):
    def __init__(self, dim_embed, dim_kernel, dilation, stride=1, padding='same', encoder=True):
        super().__init__()
        if encoder:
            self.convA = nn.Conv1d(
                dim_embed, dim_embed, dim_kernel, stride=stride, padding=padding, dilation=dilation, groups=1
            )
            self.convB = nn.Conv1d(
                dim_embed, dim_embed, dim_kernel, stride=stride, padding=padding, dilation=dilation, groups=1
            )
        else:
            self.convA = nn.ConvTranspose1d(
                dim_embed, dim_embed, dim_kernel, stride=stride, padding=0, dilation=dilation, groups=1
            )
            self.convB = nn.ConvTranspose1d(
                dim_embed, dim_embed, dim_kernel, stride=stride, padding=0, dilation=dilation, groups=1
            )

    def forward(self, x, output_size=None):
        A = self.convA(x)
        B = self.convB(x)
        x = A * F.sigmoid(B)
        # x = x + A * F.sigmoid(B)
        if output_size is not None:
            x = F._adaptive_max_pool1d(x, output_size)
        return x


class ConvEncoderBlock(nn.Module):
    def __init__(
        self, dim_embed, dim_kernel, dilation, n_heads, stride=1, padding='same', activation=nn.GELU, do_pre_norm=True
    ):
        super().__init__()
        self.do_pre_norm = do_pre_norm
        self.kernel_size = dim_kernel
        self.conv = nn.Conv1d(
            dim_embed,
            dim_embed,
            dim_kernel,
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=n_heads,
        )
        self.ff = convMLP(dim_embed)
        self.conv_norm = ConvLayerNorm(dim_embed)
        self.ff_norm = ConvLayerNorm(dim_embed)

    def forward(self, x):
        # batch, embed_size, seq_len
        B, E, S = x.shape

        if self.kernel_size > S:
            x = F.pad(x, (0, self.kernel_size - S))
        if self.do_pre_norm:
            x = x + self.conv(self.conv_norm(x))
            x = x + self.ff(self.ff_norm(x))
        else:
            x = x + self.conv_norm(self.conv(x))
            x = x + self.ff_norm(self.ff(x))
        return x


class ConvDecoderBlock(nn.Module):
    def __init__(
        self, dim_embed, dim_kernel, dilation, n_heads, stride=1, padding=0, activation=nn.GELU, do_pre_norm=True
    ):
        super().__init__()
        self.do_pre_norm = do_pre_norm
        self.kernel_size = dim_kernel
        self.conv = nn.ConvTranspose1d(
            dim_embed,
            dim_embed,
            dim_kernel,
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=n_heads,
        )
        self.ff = convMLP(dim_embed, kernel_size=3)
        self.conv_norm = ConvLayerNorm(dim_embed)
        self.ff_norm = ConvLayerNorm(dim_embed)

    def forward(self, x):
        if self.do_pre_norm:
            c = self.conv(self.conv_norm(x))
            x = F.adaptive_avg_pool1d(x, c.shape[2]) + c
            x = x + self.ff(self.ff_norm(x))
        else:
            c = self.conv_norm(self.conv(x))
            x = F.adaptive_avg_pool1d(x, c.shape[2]) + c
            x = x + self.ff_norm(self.ff(x))
        return x


class convMLP(nn.Module):
    def __init__(self, dim_embed, dim_out=None, kernel_size=1, dim_ff=None, activation=nn.GELU, n_layers=1):
        super().__init__()
        if dim_ff is None:
            dim_ff = 4 * dim_embed
        self.net = nn.Sequential()
        dim_out = dim_out if dim_out else dim_embed

        cur_out = dim_embed
        for cur_layer in range(n_layers):
            is_last = cur_layer == n_layers - 1

            dim_in = cur_out
            cur_out = dim_out if is_last else dim_ff

            self.net.append(nn.Conv1d(dim_in, dim_ff, kernel_size, padding='same'))
            self.net.append(activation())
            self.net.append(nn.Conv1d(dim_ff, cur_out, kernel_size, padding='same'))

    def forward(self, x):
        return self.net(x)
