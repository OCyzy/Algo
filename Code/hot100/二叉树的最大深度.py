# 二叉树的最大深度：本地可运行的ACM版本。
# 输入格式：一行JSON层序数组，空位置写null，例如[1,null,2,3]；[]表示空树。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# [3,9,20,null,null,15,7]
# 示例输出（多方案题允许顺序不同）：
# 3
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
    # 算法方法放到Solution中；TreeNode只保存val、left、right等节点数据。
    def maxDepth(self, root):
        if root is None:
            return 0  # 当前根本没有节点，不是“有一个叶节点”。
        # 每次调用返回当前子树的高度，不是节点的val值。
        # 当前调用在这里等待左子树算完，拿到整数后再计算右子树。
        l_depth = self.maxDepth(root.left)
        r_depth = self.maxDepth(root.right)
        # 叶节点左右均返回0，所以叶节点返回1；往父节点返回时逐层加1。
        return max(l_depth, r_depth) + 1

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    values = json.loads(input())
    root = build_tree(values)
    print(json.dumps(Solution().maxDepth(root)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("[3,9,20,null,null,15,7]\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
