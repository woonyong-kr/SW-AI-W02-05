# DP - Triangle
# 문제 링크: https://leetcode.com/problems/triangle/description/?envType=study-plan-v2&envId=top-interview-150
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int: # type: ignore
        for i in range(len(triangle)-2, -1, -1):
            for j in range(len(triangle[i])):
                triangle[i][j] += min(triangle[i+1][j], triangle[i+1][j+1])

        return triangle[0][0]
