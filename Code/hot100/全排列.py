# 全排列：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个互不相同的整数。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 3
# 1 2 3
# 示例输出（多方案题允许顺序不同）：
# [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def permute(self, nums):
        ans = []
        path = []
        n = len(nums)
        if len(set(nums)) != n:
            raise ValueError("本题要求nums中的数字互不相同")

        def dfs(i, s):
            # i是要填写的位置，s是尚未使用的数字集合；path已有i个数字。
            if i == n:
                ans.append(path.copy())
                return
            for x in s:
                path.append(x)
                # {x}是仅含x的集合；集合差s-{x}产生新集合，不会修改本层的s。
                # 下一个位置可以从剩下的任意数字中选，不限制大小/下标顺序。
                dfs(i + 1, s - {x})
                # path是各层共用的列表，所以必须撤销本层append。
                path.pop()

        dfs(0, set(nums))
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组长度与n不一致")
    print(json.dumps(Solution().permute(nums)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("3\n1 2 3\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
