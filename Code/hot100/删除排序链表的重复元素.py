# 删除排序链表的重复元素：本地可运行的ACM版本。
# 输入格式：第一行节点数n；第二行n个节点值，空链表时第二行为空。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5
# 1 1 2 3 3
# 示例输出（多方案题允许顺序不同）：
# [1,2,3]
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
    def deleteDuplicates(self, head):
        # 本题保留每种值的一个节点，输入链表必须已经按非递减顺序排列。
        if head is None:
            return None
        cur = head
        while cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next
                # 删除后不能立刻移动cur：例如1->1->1，新的后继仍可能重复。
            else:
                cur = cur.next
        # 头节点没有删除，返回原head即可；使用dummy与是否需要return无关。
        return head

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    values = list(map(int, input().split()))
    if len(values) != n:
        raise ValueError("节点数量与n不一致")
    head = build_list(values)
    if values != sorted(values):
        raise ValueError("链表必须已经排序")
    print(json.dumps(list_values(Solution().deleteDuplicates(head))))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5\n1 1 2 3 3\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
