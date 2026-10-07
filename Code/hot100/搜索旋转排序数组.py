# 搜索旋转排序数组：本地可运行的ACM版本。
# 输入格式：第一行n target；第二行n个互不相同的旋转有序整数。输出0起始下标，找不到为-1。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 7 0
# 4 5 6 7 0 1 2
# 示例输出（多方案题允许顺序不同）：
# 4
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

# 需要先建立左右边界；这里使用左闭右闭区间寻找第一个“蓝色”位置。
class Solution:
    def search(self, nums, target):
        if not nums:
            return -1

        def is_blue(i):
            end = nums[-1]
            # <=把最后一项本身也归入右侧较小段。
            # 用target所在的段调整比较，使False在前、True在后，才能二分。
            if nums[i] <= end:
                return target > end or target <= nums[i]
            else:
                return target > end and target <= nums[i]

        left = 0
        right = len(nums) - 1
        # 搜索题必须考虑最后一个位置，也允许最终left==n（所有位置都不是蓝色）。
        while left <= right:
            mid = (left + right) // 2
            if is_blue(mid):
                right = mid - 1
            else:
                left = mid + 1
        # 二分得到的是候选位置，最后仍要确认数值等于target。
        if left == len(nums) or nums[left] != target:
            return -1
        return left

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    if len(nums) != n:
        raise ValueError("数组元素数量必须等于n")
    print(json.dumps(Solution().search(nums, target)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("7 0\n4 5 6 7 0 1 2\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
