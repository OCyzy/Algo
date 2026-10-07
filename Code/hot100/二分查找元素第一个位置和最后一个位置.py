# 二分查找元素第一个位置和最后一个位置：本地可运行的ACM版本。
# 输入格式：第一行n target；第二行n个非递减整数。输出从0开始的首末下标。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 6 8
# 5 7 7 8 8 10
# 示例输出（多方案题允许顺序不同）：
# [3,4]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

def lower_bound(nums, target):
    # 返回第一个>=target的位置；全部小于target时返回len(nums)。
    left = 0
    right = len(nums) - 1
    # 左闭右闭
    while left <= right:
        # 向下取整；比较的是nums[mid]的数值，不是下标mid本身。
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            # mid已满足条件，继续往左找；闭区间必须减1，否则可能死循环。
            right = mid - 1
    return left


class Solution:
    def searchRange(self, nums, target):
        start = lower_bound(nums, target)
        if start == len(nums) or nums[start] != target:
            return [-1, -1]
        # 对整数数组，第一个>=target+1的位置就是第一个>target的位置。
        end = lower_bound(nums, target + 1) - 1
        return [start, end]

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组元素数量必须等于n")
    print(json.dumps(Solution().searchRange(nums, target)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("6 8\n5 7 7 8 8 10\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
