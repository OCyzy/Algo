# 反转链表：本地可运行的ACM版本。
# 输入格式：第一行节点数n；第二行n个节点值，空链表时第二行为空。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5
# 1 2 3 4 5
# 示例输出（多方案题允许顺序不同）：
# [5,4,3,2,1]
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
    def reverseList(self, head):
        pre = None  # 已反转部分的头节点；初始还没有节点。
        cur = head  # 当前准备处理的节点；赋值不会复制节点。
        while cur:
            nxt = cur.next  # 改箭头之前，先记住原来的后继，避免丢失后半段。
            cur.next = pre  # 真正改变链表连接：让当前节点指向已反转的部分。
            pre = cur      # 只移动pre这个变量，不会修改任何节点的next。
            cur = nxt      # 移到之前保存的下一个待处理节点。
        # cur已经走到None；pre指向原来的尾节点，也就是新头节点。
        return pre

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    values = list(map(int, input().split()))
    if len(values) != n:
        raise ValueError("节点数量与n不一致")
    head = build_list(values)
    print(json.dumps(list_values(Solution().reverseList(head))))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5\n1 2 3 4 5\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
