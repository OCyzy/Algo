# 链表的中间节点：本地可运行的ACM版本。
# 输入格式：第一行节点数n；第二行n个节点值，空链表时第二行为空。
# 输出格式：输出从中间节点开始到末尾的值列表；偶数长度选后一个中点。
# 示例输入：
# 6
# 1 2 3 4 5 6
# 示例输出（多方案题允许顺序不同）：
# [4,5,6]
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
    def middleNode(self, head):
        slow = head
        fast = head
        # fast.next是节点或None，不是数字0；必须先确定能安全走两步。
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # 快指针到末尾时，慢指针走了一半；偶数长度返回两个中点中的后一个。
        return slow

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    values = list(map(int, input().split()))
    if len(values) != n:
        raise ValueError("节点数量与n不一致")
    head = build_list(values)
    print(json.dumps(list_values(Solution().middleNode(head))))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("6\n1 2 3 4 5 6\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
