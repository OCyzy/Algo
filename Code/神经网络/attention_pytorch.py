"""单头缩放点积自注意力（Scaled Dot-Product Self-Attention）。"""

from math import sqrt

import torch
import torch.nn as nn
import torch.nn.functional as F


class selfattention(nn.Module):
    """输入、查询、键和值都来自同一个序列的单头自注意力。

    输入形状：(batch_size, seq_len, embed_size)，输出形状与输入相同。
    为了不破坏已有调用，这里保留原来的类名selfattention。
    """

    def __init__(self, embed_size):
        super().__init__()
        if embed_size <= 0:
            raise ValueError("embed_size必须是正整数")

        self.embed_size = embed_size
        # 三个线性层把同一个输入分别投影为Q、K、V。
        self.wq = nn.Linear(embed_size, embed_size)
        self.wk = nn.Linear(embed_size, embed_size)
        self.wv = nn.Linear(embed_size, embed_size)

    @staticmethod
    def _prepare_mask(mask, scores):
        """把常用mask形状转换成能与注意力分数广播的布尔张量。

        mask中的True/1表示“可以关注”，False/0表示“屏蔽”。
        支持(batch,key_len)和(batch,query_len,key_len)。
        """
        mask = mask.to(device=scores.device, dtype=torch.bool)
        if mask.ndim == 2:
            mask = mask.unsqueeze(1)  # 对所有query复用同一个padding mask。
        if mask.ndim != scores.ndim:
            raise ValueError("mask应为(batch,key_len)或(batch,query_len,key_len)")
        return mask

    def forward(self, X, mask=None):
        if X.ndim != 3 or X.size(-1) != self.embed_size:
            raise ValueError("X形状必须是(batch_size, seq_len, embed_size)")

        q = self.wq(X)
        k = self.wk(X)
        v = self.wv(X)

        # q @ k^T得到任意两个token之间的相关性，形状为(batch,seq,seq)。
        # 除以sqrt(d_k)可防止维度较大时点积过大、softmax过于尖锐。
        scores = torch.matmul(q, k.transpose(-1, -2)) / sqrt(self.embed_size)

        prepared_mask = None
        if mask is not None:
            prepared_mask = self._prepare_mask(mask, scores)
            scores = scores.masked_fill(~prepared_mask, float("-inf"))

        weights = F.softmax(scores, dim=-1)
        # 某一整行全部被mask时，softmax会产生NaN；这里把该行权重置0。
        weights = torch.nan_to_num(weights, nan=0.0)
        if prepared_mask is not None:
            weights = weights.masked_fill(~prepared_mask, 0.0)

        # 注意力权重乘V才是最终上下文；原代码误写成return v，跳过了注意力。
        context = torch.matmul(weights, v)
        return context


if __name__ == "__main__":
    # 小型可运行示例：python attention_pytorch.py
    torch.manual_seed(0)
    model = selfattention(embed_size=8)
    x = torch.randn(2, 4, 8)
    padding_mask = torch.tensor([[1, 1, 1, 0], [1, 1, 0, 0]])
    y = model(x, padding_mask)
    print("input shape :", tuple(x.shape))
    print("output shape:", tuple(y.shape))
    print("contains NaN:", torch.isnan(y).any().item())

