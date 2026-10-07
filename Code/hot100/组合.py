# 组合：本地可运行的ACM版本。
# 输入格式：一行n k：从1到n中选k个不同数字。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 4 2
# 示例输出（多方案题允许顺序不同）：
# [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def combine(self, n, k):
        ans = []
        path = []
        if k < 0 or k > n:
            return []

        def dfs(i):
            # 已选内容在path中；下一个数从i到n之间选择。
            if len(path) == k:
                ans.append(path.copy())
                return  # 已经选够，不再继续往下选。
            d = k - len(path)  # 还需要选d个数，包括这一层要选的数。
            # 选j之后还需d-1个，后面有n-j个，因此j<=n-d+1。
            # range不包含右端点，所以右端写n-d+2。
            for j in range(i, n - d + 2):
                path.append(j)
                dfs(j + 1)
                path.pop()

        dfs(1)  # 题目数字范围是1..n，不是0..n-1。
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, k = map(int, input().split())
    print(json.dumps(Solution().combine(n, k)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("4 2\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
