# DP - House Robber
# 문제 링크: https://leetcode.com/problems/house-robber/description/?envType=study-plan-v2&envId=top-interview-150
class Solution:
    def rob(self, nums: List[int]) -> int: # type: ignore
        if not nums:
            return 0
        if len(nums) <= 2:
            return max(nums)

        visit = [0] * len(nums)
        visit[0] = nums[0]
        visit[1] = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            visit[i] = max(visit[i-1], visit[i-2] + nums[i])

        return visit[-1]
