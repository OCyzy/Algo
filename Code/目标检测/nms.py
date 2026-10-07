# nms：本地可运行的ACM版本。
# 输入格式：第一行n iou_threshold；接下来n行，每行x1 y1 x2 y2 score。
# 输出格式：保留框在原输入中的下标（从0开始），按选中顺序输出。
# 示例输入：
# 3 0.5
# 0 0 2 2 0.9
# 0 0 2 2 0.8
# 3 3 5 5 0.7
# 示例输出（多方案题允许顺序不同）：
# [0,2]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

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

    def nms(self, boxes, scores, iou_threshold=0.5):
        if len(boxes) != len(scores) or not 0 <= iou_threshold <= 1:
            raise ValueError("框与分数必须一一对应，IoU阈值在0到1之间")
        # 保存的是原始下标，方便输出后找回原框；按分数降序排列。
        # Python排序稳定，同分时按原输入顺序处理。
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        keep = []
        while order:
            # 降序序列的第0项才是最高分，不能用无参数pop()取最后的最低分。
            best_index = order.pop(0)
            keep.append(best_index)
            remaining = []
            for i in order:
                # 与已选最高分框重叠过大则抑制；恰等于阈值时这里选择保留。
                if self.rectangleIoU(boxes[best_index], boxes[i]) <= iou_threshold:
                    remaining.append(i)
            order = remaining
        # 每次从剩余框中重新挑最高分，直到全部处理完。此朴素版本最坏O(n²)。
        # 这是单类别NMS；多类别检测通常先按类别分组，再对各组分别调用。
        return keep

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n_text, threshold_text = input().split()
    n = int(n_text)
    threshold = float(threshold_text)
    if n < 0:
        raise ValueError("框数量不能为负")
    boxes = []
    scores = []
    for _ in range(n):
        row = list(map(float, input().split()))
        if len(row) != 5:
            raise ValueError("每行需要x1 y1 x2 y2 score")
        x1, y1, x2, y2, score = row
        if x1 > x2 or y1 > y2:
            raise ValueError("坐标要求x1<=x2、y1<=y2")
        boxes.append([x1, y1, x2, y2])
        scores.append(score)
    print(json.dumps(Solution().nms(boxes, scores, threshold)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("3 0.5\n0 0 2 2 0.9\n0 0 2 2 0.8\n3 3 5 5 0.7\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
