# 验证二叉搜索树：本地可运行的ACM版本。
# 输入格式：一行JSON层序数组，空位置写null，例如[1,null,2,3]；[]表示空树。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# [5,1,4,null,null,3,6]
# 示例输出（多方案题允许顺序不同）：
# false
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys
from collections import deque
from math import inf


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

# 前序遍历
class Solution:
    def isValidBST(self, root, left=-inf, right=inf):
        if root is None:
            return True
        x = root.val
        # left、right是所有祖先施加的开区间限制，不只是父节点的限制。
        # 先判断当前节点，再递归左、右子树；严格不等号排除重复值。
        return (left < x < right
                and self.isValidBST(root.left, left, x)
                and self.isValidBST(root.right, x, right))


# 中序遍历
class Solution:
    def isValidBST(self, root):
        # 每次完整验证都重新初始化，避免同一个Solution多次调用时残留上次的pre。
        pre = -inf

        def dfs(node):
            nonlocal pre  # 所有递归层共用“上一个中序访问的值”。
            if node is None:
                return True
            if not dfs(node.left):
                return False
            # 左->根->右的访问顺序，在合法BST中必须严格递增。
            if node.val <= pre:
                return False
            pre = node.val
            return dfs(node.right)

        return dfs(root)


# 后序遍历
class Solution:
    def isValidBST(self, root):
        def f(node):
            # 返回整棵子树的(最小值, 最大值)，不是只返回当前节点的值。
            if node is None:
                # 空树不影响父节点比较：左侧最大值=-inf，右侧最小值=inf。
                return inf, -inf
            l_min, l_max = f(node.left)
            r_min, r_max = f(node.right)
            if node.val <= l_max or node.val >= r_min:
                # 非法标记会让任何父节点的比较也失败，从而一直向上传递。
                return -inf, inf
            # 父节点需要知道整个范围。例如当前子树在父节点左侧，
            # 父节点要与这里的最大值比较，不能只与当前node.val比较。
            return min(l_min, node.val), max(node.val, r_max)

        return f(root)[1] != inf

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    values = json.loads(input())
    root = build_tree(values)
    print(json.dumps(Solution().isValidBST(root)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("[5,1,4,null,null,3,6]\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
        
