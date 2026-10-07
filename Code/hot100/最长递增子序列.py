# 最长递增子序列：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个整数，空数组时第二行为空。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 8
# 10 9 2 5 3 7 101 18
# 示例输出（多方案题允许顺序不同）：
# 4
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys
from functools import cache

# 用枚举的思想：从当前结尾i向前找j，满足j<i且nums[j]<nums[i]。
# 正确的状态关系是dfs(i)=max(所有合法dfs(j))+1，而不是反过来更新dfs(j)。
class Solution:
    def lengthOfLIS(self, nums):
        n = len(nums)

        @cache
        def dfs(i):
            # 返回“必须以nums[i]结尾”的最长严格递增子序列长度。
            res = 0
            for j in range(i):
                if nums[j] < nums[i]:
                    res = max(res, dfs(j))
            return res + 1  # 把当前nums[i]接在末尾；没有前驱时长度就是1。

        ans = 0
        for i in range(n):
            ans = max(ans, dfs(i))  # 最优序列可能在任意位置结束，不一定在末尾。
        return ans


# 递推，从0开始
class Solution:
    def lengthOfLIS(self, nums):
        n = len(nums)
        f = [0] * n
        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    f[i] = max(f[i], f[j])
            f[i] += 1  # 前面先选最大前驱长度，最后再统一计入自己。
        return max(f, default=0)

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组长度与n不一致")
    print(json.dumps(Solution().lengthOfLIS(nums)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("8\n10 9 2 5 3 7 101 18\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
