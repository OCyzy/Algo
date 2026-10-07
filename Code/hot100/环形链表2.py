# 环形链表2：本地可运行的ACM版本。
# 输入格式：第一行n pos；第二行n个节点值。pos从0开始，-1表示无环。
# 输出格式：环入口节点的下标；无环输出-1。
# 示例输入：
# 4 1
# 3 2 0 -4
# 示例输出（多方案题允许顺序不同）：
# 1
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
    def detectCycle(self, head):
        slow = head
        fast = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast is slow:
                # 相遇点不一定是入口。一个指针从head出发，另一个从相遇点出发，
                # 此后每次都走一步，再次相遇的位置就是环入口。
                # 原理：相遇时快指针多走整数圈，因此head到入口的距离，
                # 等于相遇点继续走到入口的距离再加若干整圈。
                while slow is not head:
                    slow = slow.next
                    head = head.next
                return slow
        return None

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
    entry = Solution().detectCycle(head)
    # 有环不能沿next无限打印；输出入口下标，通过is找到同一个节点。
    index = next((i for i, node in enumerate(nodes) if node is entry), -1)
    print(json.dumps(index))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("4 1\n3 2 0 -4\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
