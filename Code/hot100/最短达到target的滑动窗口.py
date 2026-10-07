# 最短达到target的滑动窗口：本地可运行的ACM版本。
# 输入格式：第一行n target；第二行n个正整数。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 6 7
# 2 3 1 2 4 3
# 示例输出（多方案题允许顺序不同）：
# 2
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

class Solution:
    def minsubarraylen(self, target, nums):
        # 前提：target>0，nums的元素都是正整数；有负数时窗口和不再单调。
        n = len(nums)
        left = 0
        ans = n + 1
        s = 0
        for right, x in enumerate(nums):
            s += x
            # 达标就尝试收缩左端：记录当前长度后，寻找更短的达标窗口。
            while s >= target:
                ans = min(ans, right - left + 1)
                s -= nums[left]
                left += 1
        # n+1只是“没找到”的标记；题目要求这种情况返回0。
        return ans if ans <= n else 0

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    if len(nums) != n or target <= 0 or any(x <= 0 for x in nums):
        raise ValueError("请提供n个正整数以及正数target")
    print(json.dumps(Solution().minsubarraylen(target, nums)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("6 7\n2 3 1 2 4 3\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
