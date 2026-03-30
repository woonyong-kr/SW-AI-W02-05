# DP - Word Break
# 문제 링크: https://leetcode.com/problems/word-break/description/?envType=study-plan-v2&envId=top-interview-150
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool: # type: ignore
        words = set(wordDict)
        memo = {}

        def word_check(w):
            if not w:
                return True
            
            if w in memo:
                return memo[w]
            
            for i in range(1, len(w) + 1):
                word = w[:i]
                if word in words:
                    if word_check(w[i:]):
                        memo[w] = True
                        return True
            
            memo[w] = False
            return False
            
        return word_check(s)