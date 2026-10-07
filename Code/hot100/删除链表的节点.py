# 删除链表的节点：本地可运行的ACM版本。
# 输入格式：第一行n index，index从0开始且不能是最后一位；第二行n个节点值。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 4 1
# 4 5 1 9
# 示例输出（多方案题允许顺序不同）：
# [4,1,9]
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
    def deleteNode(self, node):
        # 题目只提供待删节点，没有头节点，不能直接找到它的前驱。
        # 把后继的值搬到当前节点，再跳过后继，得到题目要求的值序列。
        # 限制：node不能是尾节点；实际移除的节点对象是它的后继。
        if node is None or node.next is None:
            raise ValueError("待删除节点必须存在且不能是尾节点")
        node.val = node.next.val
        node.next = node.next.next
        # 按题意原地修改，不需要返回新头；调用方保留的head能看到修改。

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n, index = map(int, input().split())
    values = list(map(int, input().split()))
    if len(values) != n or not 0 <= index < n - 1:
        raise ValueError("index必须是一个非尾节点的有效下标")
    head = build_list(values)
    node = head
    for _ in range(index):
        node = node.next
    Solution().deleteNode(node)
    print(json.dumps(list_values(head)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("4 1\n4 5 1 9\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
