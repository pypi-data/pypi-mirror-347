"""A general Transformer based example.

@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\L}ukasz and Polosukhin, Illia},
  journal={Advances in neural information processing systems},
  volume={30},
  year={2017}
}"""

import logging
import math
import warnings

import torch
import torch.nn.functional as F
from torch import nn
from torch.nn import TransformerDecoder, TransformerDecoderLayer, TransformerEncoder, TransformerEncoderLayer

log = logging.getLogger(__name__)


class TransformerModel(nn.Module):
    """
    Generic Transformer Model for sequence to X problems, hopefully can create any published transformer model with this.

    Parameters
    ----------
    num_src_tokens: int
        vocab-size, used in nn.Embedding(ntokens, ...)
    num_tgt_tokens: int
        Target vocab size, or classification num labels, etc.
            used for embedding tgt tensor and for final nn.Linear output layer
    same_embeddings: bool
        Whether to use the same embedding matrix for src and tgt
    emb_src: bool
        Should input src be embedded or is it already a feature tensor?
    emb_tgt: bool
        Should input tgt be embedded or is it already a feature tensor?
    pos_embeddings: {'learned', 'sinusoidal', 'none'}
        What type of positional embeddings to use
    pos_max_len: int
        If pos_embeddings != 'none' the positional embeddings need to be limited for efficiency. Will default to 10,000 for sinusoidal, but will error for learned.
            Typical values 512/1024
    emb_size: int
        Size of the embedding matrices to use
    nhead: int
        Number of head for the multi-head attention of transformers
    dim_feedforward: int
        dim_feedforward of the Transformer layers, i.e. size of the transformer layers
    num_encoder_layers: int
        number of layers on the Transformer encoder. Set to 0 to only have a decoder.
            **Note**: if 0 still adds the positional encoding to the src sentence
    num_decoder_layers: int
        same as enc_nlayers but for decoder.
            **Note**: if 0 won't add positional encoding since just return the src output
    dropout: float [0,1]
        dropout of the Transformer layers
    activation: str | Callable[[Tensor], Tensor]
        activation name for the Transformer Layers
    do_teacher_force: bool
        whether to use teach forcing for the prediction (i.e. cheat off the actual input),
            or iterative generate it off previous output (Slow)
    enc_bidirectional: bool
        Whether to apply a square subsequent mask on the encoding
    dec_bidirectional: bool
        Same but for decoder
    src_padding_idx: int
        padding idx for embedding the src tensor
    tgt_padding_idx: int
        same but for tgt
    tgt_start_idx: int|None
        The idx/value that indicates this is the start of the sequence.
            Used if `do_teacher_force` == False or `tgt` in forward is None as something
            needs to be fed into the decoder to start things off
    tgt_end_idx: int|None
        Currently unused, but for the future when we allow generating until we get the "stop word"
            which is what this will represent

    """

    def __init__(
        self,
        num_src_tokens=None,
        num_tgt_tokens=None,
        same_embeddings=True,
        emb_src=True,
        emb_tgt=True,
        pos_embeddings='sinusoidal',
        pos_max_len=None,
        emb_size=512,
        nhead=8,
        dim_feedforward=2048,
        num_encoder_layers=6,
        num_decoder_layers=6,
        dropout=0.1,
        activation=F.gelu,
        do_teacher_force=True,
        enc_bidirectional=True,
        dec_bidirectional=False,
        src_pad_idx=None,
        tgt_pad_idx=None,
        tgt_start_idx=None,
        tgt_end_idx=None,
    ):
        super().__init__()
        # Check that parameters make sense
        if emb_src and num_src_tokens is None:
            raise ValueError('If you want to embed input as src tokens, please provide num_src_tokens')

        if num_tgt_tokens is None:
            num_tgt_tokens = num_src_tokens  # For caller convenience
        if same_embeddings:
            if not emb_src:
                raise ValueError("tgt_embeddings can't copy src_embeddings because emb_src = False")
            if num_tgt_tokens != num_src_tokens:
                raise ValueError('Number of tgt and src tokens must equal if embeddings are to be reused')
            if src_pad_idx != tgt_pad_idx:
                raise ValueError('If same embeddings they should have same pad idx')

        if src_pad_idx == -1 or tgt_pad_idx == -1:
            warnings.warn('Pad idx value not going to work with Embeddings')

        if not emb_tgt and tgt_start_idx is not None:
            raise ValueError("Can't use a tgt_start_idx if we aren't embedding the target")

        if pos_embeddings == 'learned' and pos_max_len is None:
            raise ValueError('Please supply max length for learned embeddings.')
        if pos_embeddings == 'sinusoidal' and pos_max_len is None:
            pos_max_len = 10000

        # Get the activation function is just supplied a name
        if isinstance(activation, str):
            self.activation = getattr(F, activation)
        else:
            self.activation = activation

        # Save parameters
        self.do_teacher_force = do_teacher_force
        self.enc_bidirectional = enc_bidirectional
        self.dec_bidirectional = dec_bidirectional
        self.emb_size = emb_size
        self.sPadIdx = src_pad_idx
        self.tPadIdx = tgt_pad_idx
        self.tgt_start_idx = tgt_start_idx
        self.tgt_end_idx = tgt_end_idx
        self.pos_embed_type = pos_embeddings

        # Setup token embeddings
        if emb_src:
            self.src_embeddings = nn.Embedding(num_src_tokens, self.emb_size, padding_idx=self.sPadIdx)
        else:
            self.src_embeddings = nn.Identity()

        if same_embeddings:
            self.tgt_embeddings = self.src_embeddings
        else:
            # Because of the way self.proj works, we need to create an embedding either way
            proj = nn.Embedding(num_tgt_tokens, self.emb_size, padding_idx=self.tPadIdx)
            if emb_tgt:
                self.tgt_embeddings = proj
            else:
                self.tgt_embeddings = nn.Identity()
                self.tgt_embeddings.weight = proj.weight  # For use in self.proj

        # Setup positional embeddings

        if self.pos_embed_type == 'learned':
            self.pos_embeddings = nn.Embedding(pos_max_len + 1, self.emb_size, padding_idx=0)
        elif self.pos_embed_type == 'sinusoidal':
            self.pos_encoder = PositionalEncoding(self.emb_size, dropout, max_len=pos_max_len)
        else:
            assert self.pos_embed_type == 'none'

        # Setup network
        ## Because often the tgt is teacher forced, given, unknown, etc. if the decoder nlayers is 0 PyTorch
        ##   will return the tgt, but we want to return the memory
        self.skip_enc, self.skip_dec = False, False

        if num_encoder_layers == 0:
            self.skip_enc = True
        else:
            enc_layers = TransformerEncoderLayer(emb_size, nhead, dim_feedforward, dropout, activation)
            self.enc = TransformerEncoder(enc_layers, num_encoder_layers)

        if num_decoder_layers == 0:
            self.skip_dec = True
        else:
            dec_layers = TransformerDecoderLayer(emb_size, nhead, dim_feedforward, dropout, activation)
            self.dec = TransformerDecoder(dec_layers, num_decoder_layers)

        # Setup output
        self.out = nn.Linear(self.emb_size, self.emb_size)
        self.out_norm = nn.LayerNorm(self.emb_size)
        self.proj_bias = nn.Parameter(torch.zeros(num_tgt_tokens))

        self._reset_parameters()  # https://github.com/pytorch/pytorch/issues/72253

    def _reset_parameters(self):
        if not self.skip_enc:
            for layer in self.enc.layers:
                layer.self_attn._reset_parameters()
                layer.linear1.reset_parameters()
                layer.linear2.reset_parameters()
                layer.norm1.reset_parameters()
                layer.norm2.reset_parameters()
        if not self.skip_dec:
            for layer in self.dec.layers:
                layer.multihead_attn._reset_parameters()
                layer.self_attn._reset_parameters()
                layer.linear1.reset_parameters()
                layer.linear2.reset_parameters()
                layer.norm1.reset_parameters()
                layer.norm2.reset_parameters()
                layer.norm3.reset_parameters()
        if isinstance(self.src_embeddings, nn.Embedding):
            self.src_embeddings.reset_parameters()
        if isinstance(self.tgt_embeddings, nn.Embedding):
            self.tgt_embeddings.reset_parameters()
        self.out.reset_parameters()
        self.out_norm.reset_parameters()
        torch.nn.init.zeros_(self.proj_bias)

    def forward(self, x):
        """
        Parameters
        ----------
        x: dict | LongTensor[n_samples, seq_len]
            `src`: LongTensor[n_samples, seq_len]
                Required, the input sequence.
            `tgt`: LongTensor[n_samples, seq_len]
                Sequence to use for teacher forcing.
            `mask`: LongTensor[n_samples, seq_len]
                If you want to filter out the projection.
        """
        if isinstance(x, dict):
            src = x.get('src')
            tgt = x.get('tgt', None)
            mask = x.get('mask', None)
        else:
            src = x
            tgt, mask = None, None

        # Sequence First
        src = src.transpose(0, 1)
        if tgt is not None:
            tgt = tgt.transpose(0, 1)

        enc = self.encode(src)
        out = self.decode(tgt, enc)
        if self.do_teacher_force:
            return self.proj(out, mask)
        return out

    def encode(self, x):
        """X should be (sequence_length, batch_size, d_model)."""
        pad_mask = None if self.sPadIdx is None else x.eq(self.sPadIdx).transpose(0, 1)
        x = self.embed(x, self.sPadIdx, self.src_embeddings)
        if self.skip_enc:
            return x
        src_mask = None
        if not self.enc_bidirectional:
            src_mask = self._generate_square_subsequent_mask(len(x), x.device, x.type())
        return self.enc(x, mask=src_mask, src_key_padding_mask=pad_mask)

    def decode(self, tgt, mem):
        """Tgt and mem should be (sequence_len, batch_size, d_model)."""
        if self.skip_dec:
            return mem

        if self.do_teacher_force:
            output = self.tdecode(tgt, mem)
        else:
            output = self.generate(mem, max_tgt_len=tgt.shape[0])
        return output

    def proj(self, out, mask):
        """Project back out. Utilizes the `tgt_embeddings` to save memory.
        In classification setting the tgt_embeddings just act as a final Linear layer.

        Parameters
        ----------
        out:
        mask:
            to filter the `out` tensor for computational efficiency if provided
                (i.e. we don't care about all the projects for like masked language modeling)
        """
        # Batch first
        out = out.transpose(0, 1).contiguous()  # .view(-1, self.emb_size)
        if mask is not None:
            out = out[mask, :]
        out = self.out_norm(self.activation(self.out(out)))
        return F.linear(out, self.tgt_embeddings.weight, self.proj_bias)

    def tdecode(self, tgt, mem):
        """Target decode."""
        pad_mask = None
        if tgt is None or tgt.shape[0] == 0:
            # Create at least 1 tgt value, otherwise why are we doing this?
            if self.tgt_start_idx is None:
                # If we don't have a start_idx just get a 0 vector
                warnings.warn('tgt_start_idx is None utilizing 0 tensor for decoding')
                tgt = mem.new_zeros((1, mem.shape[1], self.emb_size))
            else:
                # Otherwise create start word
                tgt = mem.new_full((1, mem.shape[1]), self.tgt_start_idx, dtype=torch.long)
                tgt = self.embed(tgt, self.tPadIdx, self.tgt_embeddings)
        else:
            pad_mask = None if self.tPadIdx is None else tgt.eq(self.tPadIdx).transpose(0, 1)
            tgt = self.embed(tgt, self.tPadIdx, self.tgt_embeddings)

        tgt_mask = None
        if not self.dec_bidirectional:
            tgt_mask = self._generate_square_subsequent_mask(len(tgt), tgt.device, tgt.type())
        return self.dec(tgt, mem, tgt_mask=tgt_mask, tgt_key_padding_mask=pad_mask)
        # dec is (seq_len, batch, decoder_emb_size)

    def embed(self, x, pad_idx, embeddings):
        """Handle the embedding."""
        if self.pos_embed_type == 'learned':
            return embeddings(x) + self.pos_embeddings(make_positions(x, pad_idx, seq_dim=0))
        if self.pos_embed_type == 'sinusoidal':
            x = embeddings(x) * math.sqrt(self.emb_size)
            return self.pos_encoder(x)
        return embeddings(x)

    def generate(self, mem, max_tgt_len=None):
        """
        Unwind decoding so feeds in output to next "timestep" very inefficient
          as repeats calls across the whole history. I think that's a
          limitation of the arch though.

        Parameters
        ----------
        mem - Encoder values (src_seq_len, batch, emb_size)
        """
        assert isinstance(self.tgt_embeddings, nn.Embedding)
        seq_len, batch_size, _ = mem.shape
        if max_tgt_len is None:
            max_tgt_len = seq_len

        # targets holds idxs of targets (seq_len, batch_size)
        #     tdecode handles the the start word
        targets = mem.new_empty((0, batch_size), dtype=torch.long)

        # To accumulate raw predictions (batch_size, tgt_seq_len, out_dim)
        outputs = torch.zeros(batch_size, 0, self.tgt_embeddings.weight.shape[0]).to(mem.device)
        for i in range(max_tgt_len):
            dec = self.tdecode(targets[:i], mem)

            # only care about latest one
            out = self.proj(dec[-1, :, :].unsqueeze(0), None)
            outputs = torch.cat((outputs, out[:, -1:, :]), dim=1)
            # Get actual label prediction
            # Could do a beam search or multinomial
            _, indx = out.max(dim=-1)
            # probs = F.softmax(out, dim=-1)
            # indx = torch.multinomial(probs, num_samples=1)
            # reshape so we can cat
            pred = indx[:, -1].unsqueeze(0)
            targets = torch.cat((targets, pred))

        # return actual values but flatten and remove padded values
        # assert len(outputs.view(-1,self.out.out_features)) == len(tgt_pad_mask.view(-1))
        return outputs

    def _generate_square_subsequent_mask(self, sz, device, tensor_type):
        return torch.triu(torch.full((sz, sz), float('-inf'), device=device), diagonal=1).type(tensor_type)


class PositionalEncoding(nn.Module):
    """Sinusoidal encoding.

    See: https://pytorch.org/tutorials/beginner/transformer_tutorial.html
    """

    def __init__(self, d_model, dropout=0.1, max_len=10000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[: x.size(0), :]
        return self.dropout(x)


def make_positions(x, pad_idx, seq_dim=1):
    """
    Replace non-padding symbols with their position numbers.
    Padding positions are 0 in returned tensor.

    Parameters
    ----------
    x: LongTensor
        original sequence idxs
    pad_idx: int | None
        Which values to zero
    """
    if pad_idx is None:
        return torch.cumsum(x.new_ones(x.shape), dim=seq_dim)
    mask = x.ne(pad_idx).int()
    return torch.cumsum(mask, dim=seq_dim).long() * mask


# def test_make_positions_replaces_non_padding_symbols_with_positions_number():
#    x = torch.tensor([[9, 8, 7, 6]], dtype=torch.long)
#    make_positions(x, pad_idx=None)
#    assert False
