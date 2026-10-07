# 括号生成：本地可运行的ACM版本。
# 输入格式：一行非负整数n，表示括号对数。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 3
# 示例输出（多方案题允许顺序不同）：
# ["((()))","(()())","(())()","()(())","()()()"]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def generateParenthesis(self, n):
        if n < 0:
            raise ValueError("括号对数不能为负")
        ans = []
        path = []
        m = n * 2

        def dfs(i, open):
            # i是已填写的字符数，open是已放的左括号总数，并非未匹配的数量。
            if len(path) == m:
                # join把字符列表连接成新字符串，字符串不需要也没有copy()方法。
                ans.append(''.join(path))
                return
            close = i - open  # 已放的右括号数。
            if open < n:
                path.append('(')
                dfs(i + 1, open + 1)
                path.pop()
            # 必须是另一个if而非else：两种选择可能都合法，要分别探索。
            # 右括号不能超过左括号，否则前缀已经不合法，后面也救不回来。
            if close < open:
                path.append(')')
                dfs(i + 1, open)
                path.pop()

        dfs(0, 0)
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    print(json.dumps(Solution().generateParenthesis(n)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("3\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
