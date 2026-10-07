# 01背包问题：本地可运行的ACM版本。
# 输入格式：第一行n capacity；第二行n个正整数重量；第三行n个整数价值。允许不装满。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 3 4
# 1 3 4
# 15 20 30
# 示例输出（多方案题允许顺序不同）：
# 35
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def zero_one_knapsack(self, c, w, v):
        if c < 0 or len(w) != len(v) or any(x <= 0 for x in w):
            raise ValueError("容量非负，重量为正，重量和价值一一对应")
        n = len(w)
        # dfs有两个会变化的参数，必须按(i,c)一起缓存，不能只按i缓存。
        cache = {}

        def dfs(i, c):
            # 只从下标0..i的物品中选，容量不超过c，返回最大价值。
            if i < 0:
                return 0  # 没有物品可选；本题无需恰好装满，因此空方案价值0。
            if (i, c) in cache:
                return cache[i, c]
            if w[i] > c:
                res = dfs(i - 1, c)
            else:
                # 不选：跳过i。选：拿一件i，剩余只能从0..i-1中选。
                # 两分支都i-1保证每件物品最多用一次。
                res = max(dfs(i - 1, c), dfs(i - 1, c - w[i]) + v[i])
            cache[i, c] = res
            return res

        return dfs(n - 1, c)

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, capacity = map(int, input().split())
    w = list(map(int, input().split()))
    v = list(map(int, input().split()))
    if len(w) != n or len(v) != n:
        raise ValueError("重量、价值数量必须都等于n")
    print(json.dumps(Solution().zero_one_knapsack(capacity, w, v)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("3 4\n1 3 4\n15 20 30\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
