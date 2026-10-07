# 编辑距离：本地可运行的ACM版本。
# 输入格式：两行字符串s、t，不加引号；空行表示空字符串。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# horse
# ros
# 示例输出（多方案题允许顺序不同）：
# 3
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys
from functools import cache

# 将s转化为t：s[i]==t[j]时，dfs(i,j)=dfs(i-1,j-1)，最后字符相同不额外操作。
# s[i]!=t[j]时，取min(dfs(i,j-1),dfs(i-1,j),dfs(i-1,j-1))+1；
# 注意min比较三项，不是先把三项相加。
# dfs(i,j-1)对应在s末尾插入t[j]；dfs(i-1,j)对应删除s[i]；对角项对应替换。
class Solution:
    def minDistance(self, s, t):
        m = len(s)
        n = len(t)

        @cache
        def dfs(i, j):
            # 把s[:i+1]转换为t[:j+1]的最少操作次数。
            if i < 0:
                return j + 1  # s为空，插入t剩下的j+1个字符。
            if j < 0:
                return i + 1  # t为空，删除s剩下的i+1个字符。
            if s[i] == t[j]:
                return dfs(i - 1, j - 1)
            return min(dfs(i, j - 1), dfs(i - 1, j), dfs(i - 1, j - 1)) + 1

        return dfs(m - 1, n - 1)


# 递推：f[i][j]表示s前i个字符转换为t前j个字符的最少操作次数。
# 第一行不是每格都为m+1，而是f[0][j]=j；空串变成j个字符需要j次插入。
class Solution:
    def minDistance(self, s, t):
        n = len(s)
        m = len(t)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        f[0] = list(range(m + 1))  # list把range(0..m)转为[0,1,...,m]。
        for i, x in enumerate(s):
            f[i + 1][0] = i + 1  # i+1个字符变空，需要全部删除。
            for j, y in enumerate(t):
                if x == y:
                    f[i + 1][j + 1] = f[i][j]
                else:
                    # 左格：插入；上格：删除；左上格：替换。各做一次操作。
                    f[i + 1][j + 1] = min(f[i + 1][j], f[i][j + 1], f[i][j]) + 1
        return f[n][m]

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    s = input()
    t = input()
    print(json.dumps(Solution().minDistance(s, t)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("horse\nros\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
