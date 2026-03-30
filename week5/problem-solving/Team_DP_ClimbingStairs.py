# DP - Climbing Stairs
# 문제 링크: https://leetcode.com/problems/climbing-stairs/description/?envType=study-plan-v2&envId=top-interview-150

class Solution:
    def climbStairs(self, n: int) -> int:

        if n == 1:
            return 1
        if n == 2:
            return 2

        a, b = 1, 2

        for _ in range(3, n + 1):
            a, b = b, a + b

        return b
