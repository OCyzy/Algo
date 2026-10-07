# 反转链表2：本地可运行的ACM版本。
# 输入格式：第一行n left right；第二行n个节点值。位置从1开始。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5 2 4
# 1 2 3 4 5
# 示例输出（多方案题允许顺序不同）：
# [1,4,3,2,5]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys


class ListNode:
    # next保存下一个节点的引用；节点值相同不代表是同一个节点。
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values):
    # dummy只是方便建立链表的临时头节点，不属于实际数据。
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def list_values(head):
    # 将无环链表转换为列表，才能通过标准输出观察节点的连接结果。
    result = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result

class Solution:
    def revervseBetween(self, head, left, right):
        # 保留原来的方法名；left和right是从1开始的位置。
        dummy = ListNode(next=head)
        p0 = dummy
        pre = None
        # p0停在反转区间之前的节点；left=1时，它就是dummy。
        for _ in range(left - 1):
            p0 = p0.next
        cur = p0.next
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        # 循环结束：pre是区间新头，cur是区间后面的第一个节点。
        # p0.next仍指向区间原头（现在的新尾），其next还是None，必须接回后半段。
        # 例如1->[2,3,4]->5：这里先把2.next接到5，再把1.next接到4。
        p0.next.next = cur
        p0.next = pre
        # dummy始终保留链表入口；p0已经移动过，p0.next不一定是整条链表的头。
        return dummy.next

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, left, right = map(int, input().split())
    values = list(map(int, input().split()))
    if len(values) != n or not 1 <= left <= right <= n:
        raise ValueError("要求节点数正确且1 <= left <= right <= n")
    head = build_list(values)
    print(json.dumps(list_values(Solution().revervseBetween(head, left, right))))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5 2 4\n1 2 3 4 5\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
