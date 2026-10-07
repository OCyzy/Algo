# threesum：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个整数。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 6
# -1 0 1 2 -1 -4
# 示例输出（多方案题允许顺序不同）：
# [[-1,-1,2],[-1,0,1]]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def threeSum(self, nums):
        # 排序会修改传入的列表；排序后才能根据和的大小移动双指针。
        nums.sort()
        ans = []

        # first是第一个指针；固定它后，再用left和right查找另外两个数
        for first in range(len(nums) - 2):
            # 排序后第一个数已经大于0，三数之和不可能再等于0
            if nums[first] > 0:
                break
            # 跳过重复的第一个数，避免重复答案
            if first > 0 and nums[first] == nums[first - 1]:
                continue

            left = first + 1
            right = len(nums) - 1
            while left < right:
                total = nums[first] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    ans.append([nums[first], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    # 跳过已经用过的相同数值，避免重复答案
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
        return ans

# 还可以优化的地方：固定first后，最小三数之和>0可以break；
# nums[first]+nums[-2]+nums[-1]<0可以continue，因为最大组合仍然太小。

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组元素数量必须等于n")
    print(json.dumps(Solution().threeSum(nums)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("6\n-1 0 1 2 -1 -4\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
