# 删除链表的倒数第n个节点：本地可运行的ACM版本。
# 输入格式：第一行length n，n是倒数位置（从1开始）；第二行length个节点值。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5 2
# 1 2 3 4 5
# 示例输出（多方案题允许顺序不同）：
# [1,2,3,5]
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
    def removeNthFromEnd(self, head, n):
        if n <= 0:
            raise ValueError("倒数位置n必须为正")
        dummy = ListNode(next=head)
        right = dummy
        left = dummy
        # right先走n步，之后两个指针保持n步距离。
        for _ in range(n):
            right = right.next
            if right is None:
                raise ValueError("n超过链表长度")
        while right.next:
            right = right.next
            left = left.next
        # right在最后一个节点时，left恰好位于待删节点的前一个位置。
        left.next = left.next.next
        return dummy.next

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    length, n = map(int, input().split())
    values = list(map(int, input().split()))
    if len(values) != length:
        raise ValueError("节点数量与length不一致")
    head = build_list(values)
    print(json.dumps(list_values(Solution().removeNthFromEnd(head, n))))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5 2\n1 2 3 4 5\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
