# 重排链表：本地可运行的ACM版本。
# 输入格式：第一行节点数n；第二行n个节点值，空链表时第二行为空。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 5
# 1 2 3 4 5
# 示例输出（多方案题允许顺序不同）：
# [1,5,2,4,3]
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
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def reverseList(self, head):
        pre = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre

    def reorderList(self, head):
        if head is None:
            return
        # 第一步找到中点；第二步从中点开始反转；第三步交替连接两条链。
        mid = self.middleNode(head)
        head2 = self.reverseList(mid)
        # 这里没有把前半段从mid前断开，两条链共享mid这个尾节点。
        # 例如1->2->3<-4<-5：head走左侧，head2从5走右侧。
        # head2到共享的mid时无需再插入，否则会重复连接甚至形成自环。
        while head2.next:
            nxt = head.next
            nxt2 = head2.next
            head.next = head2
            head2.next = nxt
            head = nxt
            head2 = nxt2
        # 题目要求原地修改，原头节点不变。不要把移动后的head当作新头返回。

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    values = list(map(int, input().split()))
    if len(values) != n:
        raise ValueError("节点数量与n不一致")
    head = build_list(values)
    Solution().reorderList(head)
    print(json.dumps(list_values(head)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("5\n1 2 3 4 5\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
        
