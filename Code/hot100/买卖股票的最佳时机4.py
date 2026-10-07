# 买卖股票的最佳时机4：本地可运行的ACM版本。
# 输入格式：第一行n k（最多k次交易）；第二行n个非负价格。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 6 2
# 3 2 6 5 0 3
# 示例输出（多方案题允许顺序不同）：
# 7
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys
from functools import cache
from math import inf

# 需要多记录交易次数上限j。本代码统一在“卖出”时计入一次完整交易：
# dfs(i,j,False)=max(dfs(i-1,j,False),dfs(i-1,j-1,True)+prices[i])；
# dfs(i,j,True)=max(dfs(i-1,j,True),dfs(i-1,j,False)-prices[i])。
# 也能约定在买入时计数，但转移和边界必须一起改，不能与卖出计数的代码混用。
# 递归边界：j<0为-inf；其余dfs(-1,j,False)=0，dfs(-1,j,True)=-inf。
class Solution:
    def maxProfit(self, k, prices):
        if k < 0:
            raise ValueError("交易次数不能为负")
        n = len(prices)

        @cache
        def dfs(i, j, hold):
            # 先排除负交易次数，否则i=-1、j=-1时可能被错误认定为可行。
            if j < 0:
                return -inf
            if i < 0:
                return -inf if hold else 0
            if hold:
                return max(dfs(i - 1, j, True), dfs(i - 1, j, False) - prices[i])
            return max(dfs(i - 1, j, False), dfs(i - 1, j - 1, True) + prices[i])

        return dfs(n - 1, k, False)


# 递推，空间优化：滚动掉“天数”这一维，时间O(nk)、额外空间O(k)。
class Solution:
    def maxProfit(self, k, prices):
        if k < 0:
            raise ValueError("交易次数不能为负")
        # 数组下标j表示“最多j-1次交易”；下标0专门表示非法的-1次。
        f = [[-inf] * 2 for _ in range(k + 2)]
        for j in range(1, k + 2):
            f[j][0] = 0
        for i, p in enumerate(prices):
            # 倒序保证f[j-1][1]仍是昨天的状态，而不是本轮刚更新的状态。
            for j in range(k + 1, 0, -1):
                f[j][1] = max(f[j][1], f[j][0] - p)
                f[j][0] = max(f[j][0], f[j - 1][1] + p)
        return f[k + 1][0]

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, k = map(int, input().split())
    prices = list(map(int, input().split()))
    if len(prices) != n or any(p < 0 for p in prices):
        raise ValueError("价格数量应等于n，且价格非负")
    print(json.dumps(Solution().maxProfit(k, prices)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("6 2\n3 2 6 5 0 3\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
