# 子集：本地可运行的ACM版本。
# 输入格式：第一行n；第二行n个互不相同的整数。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 3
# 1 2 3
# 示例输出（多方案题允许顺序不同）：
# [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys

# 每一个位置选还是不选
class Solution:
    def subset(self, nums):
        ans = []
        n = len(nums)
        path = []

        def f(i):
            # i表示下一个需要决定“选/不选”的下标；path是前i个数中已经选出的数。
            # 只有全部n个位置都做出选择才能记录答案；例如n=3时要做完三个决定。
            if i == n:
                # copy保存此刻的内容；不能直接存入之后还会append/pop的同一个列表。
                ans.append(path.copy())
                return
            # 不选：path不变，但当前位置已经决定好了，继续决定下一个位置。
            f(i + 1)
            # 选：先加入当前数，再在这个选择的基础上决定后面的数。
            path.append(nums[i])
            f(i + 1)
            # 递归返回到调用的下一行；撤销本层加入的数，让其他分支不受影响。
            path.pop()

        f(0)
        return ans


# 每个位置确定基于这个位置再有哪些选择：枚举“下一个选谁”。
# i到n-1是可选的下标范围，j是这次选中的下标；可以跳过元素。
# 与分割字符串的“放逗号”不同，子集不要求把所有元素切成连续的段。
class Solution:
    def subset(self, nums):
        ans = []
        n = len(nums)
        path = []

        def f(i):
            # 当前path本身就是一个完整子集，哪怕后面一个数也不选。
            ans.append(path.copy())
            if i == n:
                return
            for j in range(i, n):
                path.append(nums[j])
                # 已经选了下标j；下一个只能从j+1之后选，避免重复和倒序组合。
                f(j + 1)
                # 子调用结束，撤销本次选的nums[j]，然后for继续试下一个j。
                path.pop()

        f(0)
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组长度与n不一致")
    print(json.dumps(Solution().subset(nums)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("3\n1 2 3\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
