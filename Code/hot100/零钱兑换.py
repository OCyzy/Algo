# 零钱兑换：本地可运行的ACM版本。
# 输入格式：第一行n amount；第二行n种正整数硬币面额，每种可无限使用。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 3 11
# 1 2 5
# 示例输出（多方案题允许顺序不同）：
# 3
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys
from math import inf

class Solution:
    def coinChange(self, coins, amount):
        if amount < 0 or any(x <= 0 for x in coins):
            raise ValueError("金额非负，硬币面额必须为正")
        n = len(coins)
        cache = {}

        def dfs(i, c):
            # 只使用前i+1种硬币，恰好凑成金额c所需的最少硬币数。
            if i < 0:
                # 凑0元不需任何硬币，所以返回0，而不是“方案数”的1。
                # 金额非0却没有硬币可用表示无解，用inf避免被min误选。
                return 0 if c == 0 else inf
            if (i, c) in cache:
                return cache[i, c]
            if c < coins[i]:
                res = dfs(i - 1, c)
            else:
                # 不用这种硬币；或先用一枚（+1），剩余金额仍可用同种硬币。
                res = min(dfs(i - 1, c), dfs(i, c - coins[i]) + 1)
            cache[i, c] = res
            return res

        ans = dfs(n - 1, amount)
        return ans if ans < inf else -1


# 一维数组，容量可以正向递推：允许本轮同一种硬币使用多次（完全背包）。
class Solution:
    def coinChange(self, coins, amount):
        if amount < 0 or any(x <= 0 for x in coins):
            raise ValueError("金额非负，硬币面额必须为正")
        f = [inf] * (amount + 1)
        f[0] = 0  # 空选择凑0元；其他金额起初还无法凑出。
        for x in coins:
            for c in range(x, amount + 1):
                # 原f[c]：不用当前面额时的最少数量。
                # f[c-x]+1：先凑c-x元，再添一枚x元；取两者更少的。
                # 正序让f[c-x]可以已经包含当前面额，因此支持重复使用。
                f[c] = min(f[c], f[c - x] + 1)
        ans = f[amount]
        return ans if ans < inf else -1

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, amount = map(int, input().split())
    coins = list(map(int, input().split()))
    if len(coins) != n:
        raise ValueError("硬币种类数与n不一致")
    print(json.dumps(Solution().coinChange(coins, amount)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("3 11\n1 2 5\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
