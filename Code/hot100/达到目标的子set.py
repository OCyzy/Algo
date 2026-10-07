# 达到目标的子set：本地可运行的ACM版本。
# 输入格式：第一行n k；第二行n个正整数，统计乘积严格小于k的连续子数组。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 4 100
# 10 5 2 6
# 示例输出（多方案题允许顺序不同）：
# 8
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def numSubarrayProdectLessThanK(self, nums, k):
        # 原方法名保留。本题统计的是连续子数组，不是可以跳着取元素的子集。
        # nums均为正整数，故最小乘积为1；k<=1时没有严格小于k的窗口。
        if k <= 1:
            return 0
        left = 0
        prod = 1
        ans = 0
        for right, x in enumerate(nums):
            prod *= x
            while prod >= k:
                # prod是当前窗口整数的乘积，整除能精确撤销左端元素，避免浮点误差。
                prod //= nums[left]
                left += 1
            # 固定右端right，起点可以是left..right，共right-left+1个子数组。
            ans += right - left + 1
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, k = map(int, input().split())
    nums = list(map(int, input().split()))
    if len(nums) != n or any(x <= 0 for x in nums):
        raise ValueError("nums必须包含n个正整数")
    print(json.dumps(Solution().numSubarrayProdectLessThanK(nums, k)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("4 100\n10 5 2 6\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
