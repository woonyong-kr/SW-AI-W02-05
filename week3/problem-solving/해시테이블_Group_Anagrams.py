#https://leetcode.com/problems/group-anagrams/description/?envType=study-plan-v2&envId=top-interview-150

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        result = {}
        for s in strs:
            key = "".join(sorted(s))
            if key not in result:
                result[key] = []
                
            result[key].append(s)

        return list(result.values())
        