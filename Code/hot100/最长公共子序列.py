# 最长公共子序列：本地可运行的ACM版本。
# 输入格式：两行字符串，分别为s和t，不加引号；空行表示空字符串。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# abcde
# ace
# 示例输出（多方案题允许顺序不同）：
# 3
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys
from functools import cache

# s[i]和t[j]是两个字符；dfs(i,j)表示s[:i+1]与t[:j+1]的最长公共子序列长度。
# 未简化时，相同字符可取max(dfs(i-1,j),dfs(i,j-1),dfs(i-1,j-1)+1)；
# 不同字符可取max(dfs(i-1,j),dfs(i,j-1),dfs(i-1,j-1))。
# 相同时前两项都不超过对角项+1；不同时前两项都不小于对角项，因而可简化。
# 所以相同字符：dfs(i,j)=dfs(i-1,j-1)+1；不同字符：max(dfs(i-1,j),dfs(i,j-1))。
class Solution:
    def longestCommonSubsequence(self, s, t):
        n = len(s)
        m = len(t)

        @cache
        def dfs(i, j):
            if i < 0 or j < 0:
                return 0  # 任意一边为空，就没有公共字符可选。
            if s[i] == t[j]:
                return dfs(i - 1, j - 1) + 1
            # 最后两个字符不相等，至少舍弃一边的末尾，取更长的结果。
            return max(dfs(i - 1, j), dfs(i, j - 1))

        return dfs(n - 1, m - 1)


# 递推：f[i][j]表示s前i个字符与t前j个字符的最长公共子序列长度。
# 第一行表示s为空，第一列表示t为空，所以第一行、第一列都初始化为0。
class Solution:
    def longestCommonSubsequence(self, s, t):
        n = len(s)
        m = len(t)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        for i, x in enumerate(s):
            for j, y in enumerate(t):
                # 字符下标i、j从0开始；对应前缀长度则是i+1、j+1。
                if x == y:
                    f[i + 1][j + 1] = f[i][j] + 1
                else:
                    f[i + 1][j + 1] = max(f[i][j + 1], f[i + 1][j])
        return f[n][m]

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    s = input()
    t = input()
    print(json.dumps(Solution().longestCommonSubsequence(s, t)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("abcde\nace\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
