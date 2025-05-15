"""General RNN model for sequence classification."""

import logging

import torch
import torch.nn.functional as F
from torch import nn

from toadstool.models.utils import gen_padding_mask

log = logging.getLogger(__name__)


class RNN_classifier(nn.Module):
    """LSTM with attention."""

    def __init__(self, vocab_size, num_classes, pad_id, embed_size=512, hidden_dim=512, num_layers=12, nhead=8):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.num_classes = num_classes

        self.pad_id = pad_id
        self.embeddings = nn.Embedding(vocab_size, embed_size, padding_idx=pad_id)
        self.lstm = nn.LSTM(embed_size, hidden_dim, num_layers=self.num_layers)
        self.attention = nn.MultiheadAttention(hidden_dim, 8)
        self.out = nn.Linear(hidden_dim, num_classes)

    def init_hidden(self, batch_size, device):
        return (
            torch.autograd.Variable(torch.randn(self.num_layers, batch_size, self.hidden_dim)).to(device),
            torch.autograd.Variable(torch.randn(self.num_layers, batch_size, self.hidden_dim)).to(device),
        )

    def forward(self, x):
        if isinstance(x, list):
            inputs, lengths = x
        else:
            inputs, lengths = x, (x != self.pad_id).sum(dim=1)
        batch_size, max_seq_len = inputs.size()

        hidden = self.init_hidden(batch_size, inputs.device)
        embedded = self.embeddings(inputs)
        self.embedded = embedded

        sorted_lengths, sorted_idxs = torch.sort(lengths, dim=0, descending=True)
        sorted_embedded = embedded[sorted_idxs]

        sorted_embedded = sorted_embedded.transpose(0, 1).contiguous()

        packed = torch.nn.utils.rnn.pack_padded_sequence(sorted_embedded, sorted_lengths.cpu())
        self.lstm.flatten_parameters()
        outputs, hidden = self.lstm(packed, hidden)

        outputs, out_lengths = torch.nn.utils.rnn.pad_packed_sequence(outputs, total_length=max_seq_len)

        # hidden[0] is shaped (RNN_layers*directions, batch_size, output_size)
        # This should be the proper way to flatten (reshape) it if we do more layers/directions
        hidden0 = hidden[0].view(self.num_layers, 1, batch_size, self.hidden_dim)
        hidden0 = hidden0[-1, :, :, :].contiguous()

        # Attention layer
        outputs_mask = gen_padding_mask(outputs.shape[0], out_lengths).to(outputs.device)

        attn, weights = self.attention(hidden0, outputs, outputs, outputs_mask)
        attn, weights = attn.squeeze(0), weights.squeeze(1)

        Y = self.out(attn)
        _, unperm_idx = sorted_idxs.sort(0)  # unsort Y
        Y = Y[unperm_idx]

        self.attn = attn[unperm_idx]
        self.attn_weights = weights[unperm_idx]

        return Y


class Attention(nn.Module):
    """Old attention module before torch supported MultiHeadAttention."""

    def __init__(self, hidden_dim):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.attn_hidden = nn.Linear(self.hidden_dim * 2, self.hidden_dim)
        self.attn = nn.Linear(self.hidden_dim, 1)

    def forward(self, hidden, outputs, outputs_lengths):
        """
        Compute the attention given a state vector and set of context vectors.

        Notation:
            B -> num_batches
            S -> padded sequence length
            H -> hidden dimension size

        Parameters
        ----------
        hidden : state tensor, shape == (B,H)
        outputs: context tensor, shape == (B,S,H)
        """
        # 1. Add the state vector to each context vector to be able to compute an attention energy
        H = hidden.repeat(1, outputs.size(1), 1)  # shape == (B,S,H)
        concat = torch.cat([H, outputs], 2)  # shape == (B,S,H*2)

        # 2. Run the concatenated tensors through a linear dense layer which will output 1 value for each context vector (the attention energy)
        energies = self.attn(F.leaky_relu(self.attn_hidden(concat)))  # shape == (B,S,1)

        # 3. mask out padding values in context vectors
        max_len = outputs.size(1)

        entire_mask = torch.zeros(energies.shape)
        for i, length in enumerate(outputs_lengths):
            mask = torch.cat((torch.ones(length), torch.zeros(max_len - length))).unsqueeze(1)
            entire_mask[i] = mask
        energies.data.masked_fill_((entire_mask == 0).to(energies.device), -float('inf'))

        # 4. Softmax the attention energies along the sequences in each context vector
        weights = F.softmax(energies, dim=1)

        # 5. Apply these weights to each context vector and sum to create a new single context vector
        out = torch.bmm(outputs.transpose(1, 2), weights)  # shape == (B,H,S) * (B,S,1) == (B,H,1)
        return out.squeeze(2), weights
