# N皇后：本地可运行的ACM版本。
# 输入格式：一行非负整数n，表示n×n棋盘。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 示例输入：
# 4
# 示例输出（多方案题允许顺序不同）：
# [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
# 保留全部同名Solution：Python默认使用最后一个。比较其他解法时，注释掉后面的整个class即可。
import json
import sys

class Solution:
    def solveQueens(self, n):
        if n < 0:
            raise ValueError("棋盘大小不能为负")
        ans = []
        col = [0] * n  # col[r]保存第r行皇后所处的列。

        def valid(r, c):
            # 每行只放一枚皇后；s已经保证不重列，这里只检查两种对角线。
            for R in range(r):
                C = col[R]
                if R + C == r + c or R - C == r - c:
                    return False
            return True

        def dfs(r, s):
            # r是当前要放皇后的行，s是未使用的列集合。
            if r == n:
                # 用列表推导式立即保存棋盘；不能存入延迟执行的生成器。
                ans.append(['.' * c + 'Q' + '.' * (n - 1 - c) for c in col])
                return
            for c in s:
                if valid(r, c):
                    col[r] = c
                    dfs(r + 1, s - {c})
                    # col固定长度，后续会覆盖；s-{c}也是新集合，不需要恢复。

        dfs(0, set(range(n)))
        return ans


# 优化valid函数的for循环：建立列标记和两个对角线布尔数组，O(1)判断冲突。
class Solution:
    def solveQueens(self, n):
        if n < 0:
            raise ValueError("棋盘大小不能为负")
        ans = []
        col = [0] * n
        on_path = [False] * n
        diag1 = [False] * max(0, 2 * n - 1)
        diag2 = [False] * max(0, 2 * n - 1)

        def dfs(r):
            if r == n:
                ans.append(['.' * c + 'Q' + '.' * (n - 1 - c) for c in col])
                return
            for c in range(n):
                # r+c相同或r-c相同表示同一条对角线；加n-1把负下标平移到非负。
                d1, d2 = r + c, r - c + n - 1
                if not on_path[c] and not diag1[d1] and not diag2[d2]:
                    col[r] = c
                    on_path[c] = diag1[d1] = diag2[d2] = True
                    dfs(r + 1)
                    # 标记数组会影响后续分支的判断，必须恢复成进入本分支之前的状态。
                    on_path[c] = diag1[d1] = diag2[d2] = False

        dfs(0)
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    n = int(input())
    print(json.dumps(Solution().solveQueens(n)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("4\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
