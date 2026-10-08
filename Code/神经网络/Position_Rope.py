"""RoPE（Rotary Position Embedding）旋转位置编码。"""

import torch
import torch.nn as nn


class Position_rope(nn.Module):
    """对相邻两维组成的二维向量进行与位置相关的旋转。

    输入、输出形状为(batch_size, seq_len, d_model)，d_model必须为偶数。
    实际Transformer通常把RoPE应用到分头后的Q和K，因此这里的d_model
    也可以理解为每个注意力头的head_dim。
    """

    def __init__(self, d_model, device=None, base=10000.0):
        super().__init__()
        if d_model <= 0 or d_model % 2 != 0:
            raise ValueError("RoPE要求d_model是正偶数")
        if base <= 0:
            raise ValueError("base必须为正数")

        self.d_model = d_model
        self.base = base

        # 标准频率：theta_i = base^(-2i/d_model)。
        # arange(0,d_model,2)/d_model正好对应指数2i/d_model。
        inv_freq = 1.0 / (
            base ** (
                torch.arange(0, d_model, 2, dtype=torch.float32, device=device)
                / d_model
            )
        )
        # buffer会跟随模块移动设备，但不会被训练。
        self.register_buffer("inv_freq", inv_freq)

    def forward(self, x, start_pos=0):
        if x.ndim != 3 or x.size(-1) != self.d_model:
            raise ValueError("x形状必须是(batch_size, seq_len, d_model)")
        if not x.is_floating_point():
            raise TypeError("RoPE输入必须是浮点张量")
        if start_pos < 0:
            raise ValueError("start_pos不能为负")

        seq_len = x.size(1)
        # start_pos用于KV Cache增量推理：新token的位置不一定从0开始。
        positions = torch.arange(
            start_pos,
            start_pos + seq_len,
            dtype=self.inv_freq.dtype,
            device=x.device,
        )
        angles = torch.outer(positions, self.inv_freq)
        # (1,seq_len,d_model/2)，在batch维自动广播。
        cos = angles.cos().unsqueeze(0).to(dtype=x.dtype)
        sin = angles.sin().unsqueeze(0).to(dtype=x.dtype)

        x_even = x[..., 0::2]
        x_odd = x[..., 1::2]

        # 对每对维度(x_even,x_odd)应用二维旋转矩阵：
        # [cos -sin; sin cos]。旋转只改变方向，不改变每对向量的长度。
        rotated_even = x_even * cos - x_odd * sin
        rotated_odd = x_even * sin + x_odd * cos

        x_rotated = torch.empty_like(x)
        x_rotated[..., 0::2] = rotated_even
        x_rotated[..., 1::2] = rotated_odd
        return x_rotated


if __name__ == "__main__":
    torch.manual_seed(0)
    rope = Position_rope(d_model=8)
    x = torch.randn(2, 5, 8)
    y = rope(x)
    before = x.reshape(2, 5, 4, 2).norm(dim=-1)
    after = y.reshape(2, 5, 4, 2).norm(dim=-1)
    print("input/output shape:", tuple(x.shape), tuple(y.shape))
    print("position 0 unchanged:", torch.allclose(x[:, 0], y[:, 0]))
    print("pair norms preserved :", torch.allclose(before, after, atol=1e-6))

