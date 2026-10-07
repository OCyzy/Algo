# 二叉树的最近公共祖先：本地可运行的ACM版本。
# 输入格式：第一行JSON层序数组（节点值互不相同）；第二行p q，填写树中已有的两个节点值。
# 输出格式：最近公共祖先的节点值。
# 示例输入：
# [3,5,1,6,2,0,8,null,null,7,4]
# 5 4
# 示例输出（多方案题允许顺序不同）：
# 5
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
    def lowestCommonAncestor(self, root, p, q):
        # 原题前提：p、q均在整棵树中。局部递归不一定同时包含它们。
        if root is None or root is q or root is p:
            # None表示没找到；遇到目标先把该节点向上报告。
            # 返回目标不等于立即结束所有递归，只结束当前这一次调用。
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        # 每个结果可能是None、单个目标节点，或子树里已找到的共同祖先。
        if left and right:
            return root  # 两侧各找到一个目标，当前节点就是它们的首次汇合处。
        if left:
            return left  # 只有左侧有结果，原样向上传，不要改成root。
        return right     # 只有右侧有结果就返回它；两侧都空则返回None。
        # 若一个目标是另一个的祖先，遇到该目标直接返回也正确：
        # 它已是两者最近的共同祖先，不必继续搜索它的后代。

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    values = json.loads(input())
    root = build_tree(values)
    p_value, q_value = map(int, input().split())
    # 必须找到原树上的对象；新建TreeNode(p_value)即使同值，也不是同一个节点。
    p = find_node(root, p_value)
    q = find_node(root, q_value)
    if p is None or q is None:
        raise ValueError("本题要求p、q都存在于树中，且用节点值唯一确定")
    ancestor = Solution().lowestCommonAncestor(root, p, q)
    print(json.dumps(ancestor.val if ancestor is not None else None))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("[3,5,1,6,2,0,8,null,null,7,4]\n5 4\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
