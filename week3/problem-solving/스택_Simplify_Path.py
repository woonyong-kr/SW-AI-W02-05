#https://leetcode.com/problems/simplify-path/description/?envType=study-plan-v2&envId=top-interview-150

class Solution:
    def simplifyPath(self, path: str) -> str:
        
        names = deque(path.split("/"))
        stack = []

        for name in names:
            if name == "..":
                if stack:
                    stack.pop()
                continue
            
            if name == "." or name == "":
                continue

            stack.append(name)

        return str("/" + "/".join(stack))

        
