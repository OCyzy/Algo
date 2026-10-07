# 买卖股票的最佳时机：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个非负价格。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 保留原三种解法：它们解决的是可多次交易的股票问题（LeetCode 122），不是只交易一次的121题。
# 示例输入：
# 6
# 7 1 5 3 6 4
# 示例输出（多方案题允许顺序不同）：
# 7
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys
from functools import cache
from math import inf

# 定义最大利润dfs(i,hold)：考虑到第i天结束，hold=True表示持有，False表示不持有。
# 最多同时持有一股，但可以买卖多次：卖出来自dfs(i-1,True)+prices[i]，
# 买入来自dfs(i-1,False)-prices[i]；不操作就沿用昨天同一持仓状态的利润。
# 因而dfs(i,False)=max(dfs(i-1,False),dfs(i-1,True)+prices[i])；
# dfs(i,True)=max(dfs(i-1,True),dfs(i-1,False)-prices[i])。
# 递归边界是第0天之前：dfs(-1,False)=0、dfs(-1,True)=-inf。
# 入口dfs(n-1,False)要求最后不持股、完成兑现，不需要假定它严格大于持股状态。
class Solution:
    def maxProfit(self, prices):
        n = len(prices)

        @cache
        def dfs(i, hold):
            if i < 0:
                return -inf if hold else 0
            if hold:
                return max(dfs(i - 1, True), dfs(i - 1, False) - prices[i])
            return max(dfs(i - 1, False), dfs(i - 1, True) + prices[i])

        return dfs(n - 1, False)


# 递推，行为已处理的天数，列为是否持有
class Solution:
    def maxProfit(self, prices):
        n = len(prices)
        f = [[0] * 2 for _ in range(n + 1)]
        f[0][1] = -inf  # 尚未开始交易不可能已经持有；不能错误地初始化为0。
        for i, p in enumerate(prices):
            f[i + 1][0] = max(f[i][0], f[i][1] + p)
            f[i + 1][1] = max(f[i][1], f[i][0] - p)
        return f[n][0]


# 递推，空间复杂度进一步简化
class Solution:
    def maxProfit(self, prices):
        f0 = 0
        f1 = -inf
        for p in prices:
            # 两个新状态都应来自昨天；先暂存new_f0，避免提前覆盖旧f0。
            new_f0 = max(f0, f1 + p)
            f1 = max(f0 - p, f1)
            f0 = new_f0
        return f0

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
        sys.stdin = StringIO("6\n7 1 5 3 6 4\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
