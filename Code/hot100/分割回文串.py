# 分割回文串：本地可运行的ACM版本。
# 输入格式：一行字符串，不加引号；空行表示空字符串。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# aab
# 示例输出（多方案题允许顺序不同）：
# [["a","a","b"],["aa","b"]]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def partition(self, s):
        ans = []
        path = []
        n = len(s)

        def dfs(i):
            # s[:i]已经分割好；现在要从i开始选下一段，不能漏掉任何字符。
            if i == n:
                ans.append(path.copy())
                return
            for j in range(i, n):
                # 在下标j之后“放逗号”：取i到j（含j），切片右端需要写j+1。
                t = s[i:j + 1]
                # 当前段不回文就继续增大j，例如'ab'失败后仍会检查'aba'。
                if t == t[::-1]:
                    path.append(t)
                    # 保留已选的这一段，递归分割剩下的s[j+1:]。
                    dfs(j + 1)
                    path.pop()  # 撤销当前段，尝试别的分割位置。

        dfs(0)
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    s = input()
    print(json.dumps(Solution().partition(s), ensure_ascii=False))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("aab\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
