# 寻找旋转排序数组的最小值：本地可运行的ACM版本。
# 输入格式：第一行正整数n；第二行n个互不相同、由升序数组旋转得到的整数。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5
# 3 4 5 1 2
# 示例输出（多方案题允许顺序不同）：
# 1
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def findMin(self, nums):
        if not nums:
            raise ValueError("求最小值要求数组非空")
        left = 0
        right = len(nums) - 2
        # nums[-1]属于较小的递增段，保留作兜底答案，只二分前n-1项。
        # 元素互不相同；最小值前面的数>nums[-1]，从最小值开始的数<=nums[-1]。
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid - 1
        # 全部比较都“太大”时，left会走到n-1，最后一项就是最小值。
        return nums[left]

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组元素数量必须等于n")
    print(json.dumps(Solution().findMin(nums)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5\n3 4 5 1 2\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
