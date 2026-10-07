# 矩形相交求iou：本地可运行的ACM版本。
# 输入格式：两行，每行一个矩形的x1 y1 x2 y2，空格分隔，可用小数。
# 输出格式：交并比IoU，范围0到1。
# 示例输入：
# 0 0 2 2
# 1 1 3 3
# 示例输出（多方案题允许顺序不同）：
# 0.14285714285714285
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

# 参考矩形相交，进一步求并集：两个面积之和减去交集；不相交时交集为0，同样适用。
class Solution:

    def rectangleIoU(self, rect1, rect2):
        x1, y1, x2, y2 = rect1
        m1, n1, m2, n2 = rect2
        # 交集宽/高出现负数说明该方向不相交，此时应截断为0。
        intersection_area = (max(0, min(x2, m2) - max(x1, m1))
                             * max(0, min(y2, n2) - max(y1, n1)))
        rect1_area = (x2 - x1) * (y2 - y1)
        rect2_area = (m2 - m1) * (n2 - n1)
        # 两面积相加重复计算了一次交集，所以并集要减去交集。
        union_area = rect1_area + rect2_area - intersection_area
        # 本脚本使用连续坐标，宽高不加1；两个零面积框的IoU约定为0。
        IoU = intersection_area / union_area if union_area > 0 else 0
        return IoU

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    rect1 = list(map(float, input().split()))
    rect2 = list(map(float, input().split()))
    for rect in (rect1, rect2):
        if len(rect) != 4 or rect[0] > rect[2] or rect[1] > rect[3]:
            raise ValueError("矩形必须为x1 y1 x2 y2，且x1<=x2、y1<=y2")
    print(json.dumps(Solution().rectangleIoU(rect1, rect2)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("0 0 2 2\n1 1 3 3\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
