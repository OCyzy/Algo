"""Transformer中的固定正弦/余弦绝对位置编码。"""

import math

import torch
import torch.nn as nn


class Position_finite(nn.Module):
    """生成固定位置编码，并在forward中加到词向量上。

    输入和输出形状都是(batch_size, seq_len, d_model)。
    位置编码是buffer而不是可训练参数：会跟随model.to(device)移动，
    也会进入state_dict，但优化器不会更新它。
    """

    def __init__(self, d_model, max_len=80):
        super().__init__()
        if d_model <= 0 or max_len <= 0:
            raise ValueError("d_model和max_len必须是正整数")

        self.d_model = d_model
        self.max_len = max_len

        # position: (max_len,1)，div_term: 偶数维所使用的不同频率。
        position = torch.arange(max_len, dtype=torch.float32).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2, dtype=torch.float32)
            * (-math.log(10000.0) / d_model)
        )

        pe = torch.zeros(max_len, d_model, dtype=torch.float32)
        pe[:, 0::2] = torch.sin(position * div_term)
        # 奇数d_model时，奇数位置的列数会少1，因此截取对应数量的频率。
        odd_columns = pe[:, 1::2].shape[1]
        pe[:, 1::2] = torch.cos(position * div_term[:odd_columns])

        # 增加batch维后是(1,max_len,d_model)，可广播到任意batch_size。
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x):
        if x.ndim != 3 or x.size(-1) != self.d_model:
            raise ValueError("x形状必须是(batch_size, seq_len, d_model)")
        seq_len = x.size(1)
        if seq_len > self.max_len:
            raise ValueError(f"序列长度{seq_len}超过max_len={self.max_len}")

        # 只取本次实际长度，并转换成与x相同的dtype。
        return x + self.pe[:, :seq_len].to(dtype=x.dtype)


if __name__ == "__main__":
    encoding = Position_finite(d_model=8, max_len=20)
    x = torch.zeros(2, 5, 8)
    y = encoding(x)
    print("input/output shape:", tuple(x.shape), tuple(y.shape))
    print("position 0       :", y[0, 0].tolist())
    print("trainable params :", sum(p.numel() for p in encoding.parameters()))

