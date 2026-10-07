# 打家劫舍：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个整数，空数组时第二行为空。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5
# 2 7 9 3 1
# 示例输出（多方案题允许顺序不同）：
# 12
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys

class Solution:
    def rob(self, nums):
        n = len(nums)
        cache = [-1] * n

        def dfs(i):
            # dfs(i)：只考虑下标0..i的房屋，可以获得的最大金额。
            if i < 0:
                return 0
            if cache[i] != -1:
                return cache[i]
            # 不偷i就看前i-1；偷i就跳过相邻的i-1，再加上nums[i]。
            res = max(dfs(i - 1), dfs(i - 2) + nums[i])
            cache[i] = res
            return res

        return dfs(n - 1)


# 优化空间复杂度O(n)到O(1)，从前到后直接迭代
class Solution:
    def rob(self, nums):
        f0 = f1 = 0
        for i, x in enumerate(nums):
            # 更新前：f0对应dfs(i-2)，f1对应dfs(i-1)。
            new_f = max(f1, f0 + x)
            f0 = f1
            f1 = new_f  # 更新后，两个状态一起向前挪一格。
        return f1

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组长度与n不一致")
    print(json.dumps(Solution().rob(nums)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5\n2 7 9 3 1\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
