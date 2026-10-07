# 电话号码的字母组合：本地可运行的ACM版本。
# 输入格式：一行由2到9组成的数字字符串，不加引号；空行输出[]。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 23
# 示例输出（多方案题允许顺序不同）：
# ["ad","ae","af","bd","be","bf","cd","ce","cf"]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

MAPPING = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]


class Solution:
    def letterCombinations(self, digits):
        if len(digits) == 0:
            return []
        if any(c not in "23456789" for c in digits):
            raise ValueError("电话号码只能包含数字2到9")
        n = len(digits)
        ans = []
        path = [''] * n  # 固定n个格子，每层递归只负责填写其中一个。

        def dfs(i):
            if i == n:
                ans.append(''.join(path))  # 得到独立字符串，不受以后覆盖path的影响。
                return
            # digits[i]是字符，例如'2'；int后才能按下标查到字符串'abc'。
            # 直接遍历字符串得到a、b、c；range只能接收整数，不能接收'abc'。
            for c in MAPPING[int(digits[i])]:
                path[i] = c
                dfs(i + 1)
                # 不需要pop：不是append增加长度，而是覆盖固定位置。
                # 下一分支会重新填写后续位置，填满之后才保存答案。

        dfs(0)
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    digits = input().strip()
    print(json.dumps(Solution().letterCombinations(digits)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("23\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
