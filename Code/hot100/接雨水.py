# 接雨水：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个非负柱高。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 12
# 0 1 0 2 1 0 1 3 2 1 2 1
# 示例输出（多方案题允许顺序不同）：
# 6
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        pre_max = suf_max = ans = 0
        # pre_max和suf_max分别记录从左右走到当前边界时看到的最高柱子。
        while left < right:
            pre_max = max(pre_max, height[left])
            suf_max = max(suf_max, height[right])
            # 较低的一侧水位已经能确定：另一侧至少有更高的墙挡住水。
            if pre_max > suf_max:
                ans += suf_max - height[right]
                right -= 1
            else:
                ans += pre_max - height[left]
                left += 1
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    height = list(map(int, input().split()))
    if len(height) != n:
        raise ValueError("高度数量必须等于n")
    print(json.dumps(Solution().trap(height)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("12\n0 1 0 2 1 0 1 3 2 1 2 1\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
