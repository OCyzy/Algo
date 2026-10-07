# 环形链表：本地可运行的ACM版本。
# 输入格式：第一行n pos；第二行n个节点值。尾节点连到下标pos，-1表示无环。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 4 1
# 3 2 0 -4
# 示例输出（多方案题允许顺序不同）：
# true
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
    def hasCycle(self, head):
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            # is比较“是否同一个节点对象”，不是两个节点的val是否相等。
            # 在环中，快指针相对慢指针每次多走一步，最终必然相遇。
            if fast is slow:
                return True
        return False  # 能走到None说明不存在环。

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, pos = map(int, input().split())
    values = list(map(int, input().split()))
    if len(values) != n or not -1 <= pos < n:
        raise ValueError("节点数量错误或pos越界")
    nodes = [ListNode(value) for value in values]
    for i in range(n - 1):
        nodes[i].next = nodes[i + 1]
    if pos != -1:
        nodes[-1].next = nodes[pos]
    head = nodes[0] if nodes else None
    print(json.dumps(Solution().hasCycle(head)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("4 1\n3 2 0 -4\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
