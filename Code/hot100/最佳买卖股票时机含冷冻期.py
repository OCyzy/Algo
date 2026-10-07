# 最佳买卖股票时机含冷冻期：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个非负价格；卖出后第二天不能买入。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5
# 1 2 3 0 2
# 示例输出（多方案题允许顺序不同）：
# 3
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys
from functools import cache
from math import inf

class Solution:
    def maxProfit(self, prices):
        n = len(prices)

        @cache
        def dfs(i, hold):
            # 考虑到第i天结束、指定持仓状态时的最大利润。
            if i < 0:
                return -inf if hold else 0
            if hold:
                # 今天买入就不能是昨天刚卖出，只能从前天的不持股状态转移。
                # 中间空出一天作为冷冻期；继续持有则仍然来自昨天。
                return max(dfs(i - 1, True), dfs(i - 2, False) - prices[i])
            # 今天卖出或继续不持有，都不会违反今天的买入限制。
            return max(dfs(i - 1, False), dfs(i - 1, True) + prices[i])

        return dfs(n - 1, False)

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    prices = list(map(int, input().split()))
    if len(prices) != n or any(p < 0 for p in prices):
        raise ValueError("价格数量应等于n，且价格非负")
    print(json.dumps(Solution().maxProfit(prices)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5\n1 2 3 0 2\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
