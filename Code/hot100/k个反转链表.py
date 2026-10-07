# k个反转链表：本地可运行的ACM版本。
# 输入格式：第一行n k；第二行n个节点值。k必须大于0。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5 2
# 1 2 3 4 5
# 示例输出（多方案题允许顺序不同）：
# [2,1,4,3,5]
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
    def reversKGroup(self, head, k):
        # 保留原来的方法名，补齐必须传入的组大小k。
        if k <= 0:
            raise ValueError("k必须为正整数")
        dummy = ListNode(next=head)
        n = 0
        cur = head
        while cur:
            n += 1
            cur = cur.next

        p0 = dummy  # 当前待反转组之前的那个节点。
        while n >= k:
            n -= k  # 每次处理整组k个，不是只处理一个。
            cur = p0.next
            pre = None
            for _ in range(k):
                nxt = cur.next
                cur.next = pre
                pre = cur
                cur = nxt
            # 原来的组头现在是组尾；先记住它，才能移动p0到下一组之前。
            nxt = p0.next
            p0.next.next = cur  # 新组尾接上未处理部分。
            p0.next = pre       # 前面的部分接上新组头。
            p0 = nxt            # 下一组的前驱就是这一组的新尾。
        # 最后不足k个的节点保持原顺序；它们已经通过上面的接线保留。
        return dummy.next

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, k = map(int, input().split())
    values = list(map(int, input().split()))
    if len(values) != n:
        raise ValueError("节点数量与n不一致")
    head = build_list(values)
    print(json.dumps(list_values(Solution().reversKGroup(head, k))))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5 2\n1 2 3 4 5\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
