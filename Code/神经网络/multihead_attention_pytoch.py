"""从零实现多头注意力，保留原文件名和类名。"""

from math import sqrt

import torch
import torch.nn as nn
import torch.nn.functional as F


class Multihead_attention(nn.Module):
    """标准多头注意力，可用于自注意力或交叉注意力。

    q形状为(batch, query_len, d_model)，k和v形状为
    (batch, key_len, d_model)。自注意力时q、k、v可以传同一个张量。
    """

    def __init__(self, heads, d_model, dropout=0.1):
        super().__init__()
        if heads <= 0 or d_model <= 0:
            raise ValueError("heads和d_model必须是正整数")
        if d_model % heads != 0:
            raise ValueError("d_model必须能被heads整除")

        self.d_model = d_model
        self.h = heads
        self.dk = d_model // heads  # 每个头实际拥有的特征维度。
        self.wq = nn.Linear(d_model, d_model)
        self.wk = nn.Linear(d_model, d_model)
        self.wv = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(d_model, d_model)

    @staticmethod
    def _prepare_mask(mask, scores):
        """将mask扩展到(batch, heads, query_len, key_len)。"""
        mask = mask.to(device=scores.device, dtype=torch.bool)
        if mask.ndim == 2:
            # (batch,key_len) -> (batch,1,1,key_len)。
            mask = mask.unsqueeze(1).unsqueeze(2)
        elif mask.ndim == 3:
            # (batch,query_len,key_len) -> (batch,1,query_len,key_len)。
            mask = mask.unsqueeze(1)
        elif mask.ndim != 4:
            raise ValueError("mask维度应为2、3或4")
        return mask

    def attention(self, q, k, v, dk, mask=None, dropout=None):
        # q: (batch, heads, query_len, dk)
        # k/v: (batch, heads, key_len, dk)
        scores = torch.matmul(q, k.transpose(-1, -2)) / sqrt(dk)
        # scores: (batch, heads, query_len, key_len)

        prepared_mask = None
        if mask is not None:
            prepared_mask = self._prepare_mask(mask, scores)
            scores = scores.masked_fill(~prepared_mask, float("-inf"))

        weights = F.softmax(scores, dim=-1)
        weights = torch.nan_to_num(weights, nan=0.0)
        if prepared_mask is not None:
            weights = weights.masked_fill(~prepared_mask, 0.0)
        if dropout is not None:
            weights = dropout(weights)

        return torch.matmul(weights, v)

    def _split_heads(self, x):
        """(batch, seq, d_model) -> (batch, heads, seq, dk)。"""
        batch_size, seq_len, _ = x.shape
        # 原代码最后一维误写成d_model；正确关系是heads * dk = d_model。
        return x.reshape(batch_size, seq_len, self.h, self.dk).transpose(1, 2)

    def forward(self, q, k, v, mask=None):
        if q.ndim != 3 or k.ndim != 3 or v.ndim != 3:
            raise ValueError("q、k、v都必须是三维张量")
        if q.size(0) != k.size(0) or k.size(0) != v.size(0):
            raise ValueError("q、k、v的batch_size必须相同")
        if k.size(1) != v.size(1):
            raise ValueError("k和v的序列长度必须相同")
        if any(x.size(-1) != self.d_model for x in (q, k, v)):
            raise ValueError("q、k、v最后一维必须等于d_model")

        q = self._split_heads(self.wq(q))
        k = self._split_heads(self.wk(k))
        v = self._split_heads(self.wv(v))

        context = self.attention(q, k, v, self.dk, mask, self.dropout)

        # transpose后内存通常不连续；contiguous/reshape后再拼回d_model。
        batch_size, _, query_len, _ = context.shape
        context = context.transpose(1, 2).contiguous()
        context = context.reshape(batch_size, query_len, self.d_model)
        return self.out(context)


if __name__ == "__main__":
    torch.manual_seed(0)
    model = Multihead_attention(heads=4, d_model=16, dropout=0.0)
    q = torch.randn(2, 3, 16)
    k = torch.randn(2, 5, 16)
    v = torch.randn(2, 5, 16)
    key_mask = torch.tensor([[1, 1, 1, 1, 0], [1, 1, 1, 0, 0]])
    y = model(q, k, v, key_mask)
    print("q/k/v shape:", tuple(q.shape), tuple(k.shape), tuple(v.shape))
    print("output shape:", tuple(y.shape))
    print("contains NaN:", torch.isnan(y).any().item())

