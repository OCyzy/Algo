# maxarea：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个非负柱高。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 9
# 1 8 6 2 5 4 8 3 7
# 示例输出（多方案题允许顺序不同）：
# 49
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def maxArea(self, height):
        left = 0
        right = len(height) - 1
        ans = 0
        # 面积由较短的柱子决定，宽度用下标之差；不能把下标当高度。
        while left < right:
            area = min(height[left], height[right]) * (right - left)
            ans = max(ans, area)

            # 只有移动较矮的一边，才有可能得到更大的面积。
            if height[left] <= height[right]:
                old_height = height[left]
                left += 1
                # 宽度已经变小，高度不超过原高度时，面积不可能更大。
                while left < right and height[left] <= old_height:
                    left += 1
            else:
                old_height = height[right]
                right -= 1
                while left < right and height[right] <= old_height:
                    right -= 1
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    height = list(map(int, input().split()))
    if len(height) != n:
        raise ValueError("高度数量必须等于n")
    print(json.dumps(Solution().maxArea(height)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("9\n1 8 6 2 5 4 8 3 7\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
