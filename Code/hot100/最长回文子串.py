# 最长回文子串：本地可运行的ACM版本。
# 输入格式：一行字符串；空行表示空字符串。
# 输出格式：输出一行JSON；数字、布尔值、列表都可以直接观察。
# 文件名与原代码题意不同：这里保留原方法，解决无重复字符的最长子串（第3题），不是最长回文子串。
# 示例输入：
# abcabcbb
# 示例输出（多方案题允许顺序不同）：
# 3
# 正常运行后在终端输入；运行时添加 --demo 参数可直接使用上面的示例。
import json
import sys

from collections import Counter


class Solution:
    def lengthOfLongestSubstring(self, s):
        # 保留原来的滑动窗口思路：求“无重复字符的最长子串长度”。
        # 回文要求正读反读相同，是另一道题，不能由此窗口算法求得。
        ans = 0
        left = 0
        cnt = Counter()
        for right, x in enumerate(s):
            cnt[x] += 1
            # 新加入的x重复了，就向右收缩左边界，直到窗口中每个字符至多一次。
            while cnt[x] > 1:
                cnt[s[left]] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans

def solve():
    # solve只负责输入输出；算法仍放在上面的Solution中。
    s = input()
    print(json.dumps(Solution().lengthOfLongestSubstring(s)))


if __name__ == "__main__":
    # 只有直接运行此文件时才读输入；被其他脚本import时不会等待键盘输入。
    if "--demo" in sys.argv:
        from io import StringIO
        sys.stdin = StringIO("abcabcbb\n")
    # 保留递归学习版本；较深的递归需要高于Python默认值的深度限制。
    sys.setrecursionlimit(100_000)
    solve()
