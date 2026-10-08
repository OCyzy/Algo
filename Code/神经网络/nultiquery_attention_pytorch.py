"""Multi-Query Attention：多个Q头共享同一组K/V。"""

from math import sqrt

import torch
import torch.nn as nn
import torch.nn.functional as F


class Multiquery_attention(nn.Module):
    """多查询注意力（MQA）的教学实现。

    Q仍有num_heads个头，而K、V各只有一个头。计算时利用广播让
    所有Q头共享K/V，可减少自回归推理时KV Cache的大小。
    """

    def __init__(self, embed_size, num_heads, dropout=0.1):
        super().__init__()
        if embed_size <= 0 or num_heads <= 0:
            raise ValueError("embed_size和num_heads必须是正整数")
        if embed_size % num_heads != 0:
            raise ValueError("embed_size必须能被num_heads整除")

        self.embed_size = embed_size
        self.num_heads = num_heads
        self.dk = embed_size // num_heads

        # Q输出完整embed_size，随后拆成多个头。
        self.wq = nn.Linear(embed_size, embed_size)
        # K/V只输出一个头的dk维，这是MQA节省KV存储的关键。
        self.wk = nn.Linear(embed_size, self.dk)
        self.wv = nn.Linear(embed_size, self.dk)
        self.out = nn.Linear(embed_size, embed_size)
        self.dropout = nn.Dropout(dropout)

    def split_heads(self, x, num_heads=None):
        """把最后一维拆为(num_heads, dk)，并把头维移到序列维之前。"""
        if num_heads is None:
            num_heads = self.num_heads
        batch_size, seq_len, feature_size = x.shape
        if feature_size != num_heads * self.dk:
            raise ValueError("输入最后一维必须等于num_heads * dk")
        # 正确结果：(batch, num_heads, seq_len, dk)。
        # 原代码transpose(-1,-2)会得到(batch,seq_len,dk,num_heads)。
        return x.reshape(batch_size, seq_len, num_heads, self.dk).transpose(1, 2)

    @staticmethod
    def _prepare_mask(mask, scores):
        mask = mask.to(device=scores.device, dtype=torch.bool)
        if mask.ndim == 2:
            mask = mask.unsqueeze(1).unsqueeze(2)
        elif mask.ndim == 3:
            mask = mask.unsqueeze(1)
        elif mask.ndim != 4:
            raise ValueError("mask维度应为2、3或4")
        return mask

    def forward(self, x, mask=None):
        if x.ndim != 3 or x.size(-1) != self.embed_size:
            raise ValueError("x形状必须是(batch_size, seq_len, embed_size)")

        q = self.split_heads(self.wq(x))     # (batch, heads, seq, dk)
        k = self.split_heads(self.wk(x), 1)  # (batch, 1, seq, dk)
        v = self.split_heads(self.wv(x), 1)  # (batch, 1, seq, dk)

        # k/v的头数为1，会自动广播到所有Q头，并没有真的复制num_heads份。
        scores = torch.matmul(q, k.transpose(-1, -2)) / sqrt(self.dk)

        prepared_mask = None
        if mask is not None:
            prepared_mask = self._prepare_mask(mask, scores)
            scores = scores.masked_fill(~prepared_mask, float("-inf"))

        weights = F.softmax(scores, dim=-1)
        weights = torch.nan_to_num(weights, nan=0.0)
        if prepared_mask is not None:
            weights = weights.masked_fill(~prepared_mask, 0.0)
        weights = self.dropout(weights)

        context = torch.matmul(weights, v)
        # context: (batch, heads, seq, dk)，拼接各头后恢复embed_size。
        batch_size, _, seq_len, _ = context.shape
        context = context.transpose(1, 2).contiguous()
        context = context.reshape(batch_size, seq_len, self.embed_size)
        return self.out(context)


if __name__ == "__main__":
    torch.manual_seed(0)
    model = Multiquery_attention(embed_size=16, num_heads=4, dropout=0.0)
    x = torch.randn(2, 5, 16)
    padding_mask = torch.tensor([[1, 1, 1, 1, 0], [1, 1, 1, 0, 0]])
    y = model(x, padding_mask)
    print("input shape :", tuple(x.shape))
    print("output shape:", tuple(y.shape))
    print("K/V heads   : 1 (shared by all Q heads)")

