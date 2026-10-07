# twosum：本地可运行的ACM版本。
# 输入格式：第一行n target；第二行n个已排序整数。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 4 9
# 2 7 11 15
# 示例输出（多方案题允许顺序不同）：
# [1,2]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

# 列表已经排序好（非递减）；返回的两个位置从1开始计数。
from typing import List


class Solution:
    def twosum(self, nums: List[int], target: int) -> List[int]:
        left = 0
        right = len(nums) - 1
        # left<right保证不重复使用同一个数，也让空数组安全返回。
        while left < right:
            total = nums[left] + nums[right]
            if total == target:
                return [left + 1, right + 1]
            # 有序性保证：和太大，缩小右端；和太小，增大左端。
            if total > target:
                right -= 1
            else:
                left += 1
        return []

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组元素数量必须等于n")
    print(json.dumps(Solution().twosum(nums, target)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("4 9\n2 7 11 15\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
