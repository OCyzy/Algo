# 完全背包：本地可运行的ACM版本。
# 输入格式：第一行n capacity；第二行n个正整数重量；第三行n个整数价值。允许不装满。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 3 4
# 1 3 4
# 15 20 30
# 示例输出（多方案题允许顺序不同）：
# 60
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def unbounded_knapsack(self, capacity, w, v):
        if capacity < 0 or len(w) != len(v) or any(x <= 0 for x in w):
            raise ValueError("容量非负，重量为正，重量和价值一一对应")
        n = len(w)
        cache = {}  # (物品种类上界, 剩余容量)共同确定一个子问题。

        def dfs(i, c):
            if i < 0:
                return 0
            if (i, c) in cache:
                return cache[i, c]
            if c < w[i]:
                res = dfs(i - 1, c)
            else:
                # 不选这种物品：彻底跳过i，进入i-1，不能原地调用dfs(i,c)。
                # 选一件：容量减少，但仍保留i这个种类，因此可以重复拿。
                res = max(dfs(i - 1, c), dfs(i, c - w[i]) + v[i])
            cache[i, c] = res
            return res

        return dfs(n - 1, capacity)

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, capacity = map(int, input().split())
    w = list(map(int, input().split()))
    v = list(map(int, input().split()))
    if len(w) != n or len(v) != n:
        raise ValueError("重量、价值数量必须都等于n")
    print(json.dumps(Solution().unbounded_knapsack(capacity, w, v)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("3 4\n1 3 4\n15 20 30\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
