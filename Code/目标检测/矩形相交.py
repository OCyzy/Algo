# 矩形相交：本地可运行的ACM版本。
# 输入格式：两行，每行一个矩形的x1 y1 x2 y2，空格分隔，可用小数。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 0 0 2 2
# 1 1 3 3
# 示例输出（多方案题允许顺序不同）：
# true
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

# 需要横坐标纵坐标都有交集，判断是否有交集的方式是两个区间的左端点最大值必须小于右端点最小值。
# 这里判断正面积的相交：仅接触边或角不算重叠，所以用<而不是<=。
class Solution:
    def isIntervalOverlap(self, l1, r1, l2, r2):
        return max(l1, l2) < min(r1, r2)

    def isRectangleOverlap(self, rec1, rec2):
        # 坐标约定为[x1,y1,x2,y2]，分别是左下角、右上角（连续坐标）。
        return (self.isIntervalOverlap(rec1[0], rec1[2], rec2[0], rec2[2])
                and self.isIntervalOverlap(rec1[1], rec1[3], rec2[1], rec2[3]))

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    rect1 = list(map(float, input().split()))
    rect2 = list(map(float, input().split()))
    for rect in (rect1, rect2):
        if len(rect) != 4 or rect[0] > rect[2] or rect[1] > rect[3]:
            raise ValueError("矩形必须为x1 y1 x2 y2，且x1<=x2、y1<=y2")
    print(json.dumps(Solution().isRectangleOverlap(rect1, rect2)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("0 0 2 2\n1 1 3 3\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
