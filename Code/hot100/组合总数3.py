# 组合总数3：本地可运行的ACM版本。
# 输入格式：一行k n：从1到9选k个不同数字，使它们的和为n。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 3 7
# 示例输出（多方案题允许顺序不同）：
# [[4,2,1]]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def combine(self, k, n):
        ans = []
        path = []
        if k < 0 or k > 9:
            return []

        def dfs(i, t):
            # 倒序选数：只能从1..i选；t是剩余目标和，d是还需选的个数。
            d = k - len(path)
            if d == 0:
                if t == 0:  # 个数够了还必须总和恰好够，不能只判断长度。
                    ans.append(path.copy())
                return
            # 剩余数字不足；或最小/最大可能的总和都达不到t时，提前剪枝。
            if i < d or t < d * (d + 1) // 2:
                return
            if t > (i * 2 - d + 1) * d // 2:
                return
            # 当前选j，后续只能选更小的数；j至少为d才能留够d-1个候选。
            for j in range(i, d - 1, -1):
                path.append(j)
                dfs(j - 1, t - j)
                path.pop()

        dfs(9, n)
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    k, n = map(int, input().split())
    print(json.dumps(Solution().combine(k, n)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("3 7\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
