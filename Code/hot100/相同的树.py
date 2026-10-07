# 相同的树：本地可运行的ACM版本。
# 输入格式：两行JSON层序数组，分别表示两棵树；空位置写null，空树写[]。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# [1,2,3]
# [1,2,3]
# 示例输出（多方案题允许顺序不同）：
# true
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    # 输入采用LeetCode层序格式，例如[1,null,2,3]表示2的左孩子是3。
    # 只给实际存在的节点分配左右孩子；不是按完全二叉树下标2*i+1建树。
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


def find_node(root, value):
    # 返回树中已有的节点，不能新建一个同值节点来代替：is比较对象身份。
    if root is None:
        return None
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node.val == value:
            return node
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return None

class Solution:
    def isSameTree(self, p, q):
        # 判断边界条件，左边或者右边没了
        if p is None or q is None:
            # 进入这里时至少一个为空；is只会在两者都是None时为True。
            # 这一步不是比较val；None没有val可读。
            return p is q
        # 两节点都存在时，比较值及相同方向的子树，不要求是同一个节点对象。
        return (p.val == q.val
                and self.isSameTree(p.left, q.left)
                and self.isSameTree(p.right, q.right))

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    p = build_tree(json.loads(input()))
    q = build_tree(json.loads(input()))
    print(json.dumps(Solution().isSameTree(p, q)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("[1,2,3]\n[1,2,3]\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
