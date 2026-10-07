# 目标和：本地可运行的ACM版本。
# 输入格式：第一行n target；第二行n个非负整数（允许重复与0）。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5 3
# 1 1 1 1 1
# 示例输出（多方案题允许顺序不同）：
# 5
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys
from functools import cache

class Solution:
    def findTargetSumWays(self, nums, target):

        # 正号对应的数字之和为p。
        # 负号对应的数字之和为sum(nums)-p。
        # p-sum(nums)+p = target。
        # 因此p = (target+sum(nums))/2：转化为选一些下标，恰好凑出p的方案数。
        total = sum(nums)
        if abs(target) > total:
            return 0
        target += total
        if target < 0 or target % 2 != 0:
            return 0
        p = target // 2
        n = len(nums)

        @cache
        def dfs(i, c):
            # 从0..i这些下标中选数，凑出剩余和c的方案数量；不是最少选几个。
            if i < 0:
                # 没有数可选且已经凑齐：空选择恰好是一种成功方案。
                return 1 if c == 0 else 0
            if c < nums[i]:
                return dfs(i - 1, c)
            # 选与不选当前下标是互不重叠的方案，数量直接相加。
            return dfs(i - 1, c) + dfs(i - 1, c - nums[i])

        return dfs(n - 1, p)


# 优化空间复杂度：从0开始递推，只保留相邻两行，而不是完整n行。
class Solution:
    def findTargetSumWays(self, nums, target):

        # 正号对应的数字之和为p。
        # 负号对应的数字之和为sum(nums)-p。
        # p-sum(nums)+p = target。
        # 因此p = (target+sum(nums))/2：转化为选一些下标，恰好凑出p的方案数。
        total = sum(nums)
        if abs(target) > total:
            return 0
        target += total
        if target < 0 or target % 2 != 0:
            return 0
        p = target // 2
        n = len(nums)

        f = [[0] * (p + 1) for _ in range(2)]
        f[0][0] = 1
        for i, x in enumerate(nums):
            for c in range(p + 1):
                if c < x:
                    f[(i + 1) % 2][c] = f[i % 2][c]
                else:
                    # 新行全部读取旧行，所以这里容量可以正序枚举。
                    f[(i + 1) % 2][c] = f[i % 2][c] + f[i % 2][c - x]
        return f[n % 2][p]  # 此时目标是p，不是尚未除以2的target。


# 进一步用一维数组简化，以防被覆盖所以要从后到前算
class Solution:
    def findTargetSumWays(self, nums, target):

        # 正号对应的数字之和为p。
        # 负号对应的数字之和为sum(nums)-p。
        # p-sum(nums)+p = target。
        # 因此p = (target+sum(nums))/2：转化为选一些下标，恰好凑出p的方案数。
        total = sum(nums)
        if abs(target) > total:
            return 0
        target += total
        if target < 0 or target % 2 != 0:
            return 0
        p = target // 2
        n = len(nums)

        f = [0] * (p + 1)
        f[0] = 1
        for i, x in enumerate(nums):
            for c in range(p, x - 1, -1):
                # 倒序使f[c-x]仍来自上一轮，当前下标只使用一次（01背包）。
                # x=0时f[c]翻倍：给这个0加正号和负号是两种不同表达式。
                f[c] = f[c] + f[c - x]
        return f[p]

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    if len(nums) != n or any(x < 0 for x in nums):
        raise ValueError("数字数量应等于n，且数字非负")
    print(json.dumps(Solution().findTargetSumWays(nums, target)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5 3\n1 1 1 1 1\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
