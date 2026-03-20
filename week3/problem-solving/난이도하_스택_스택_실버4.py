# 스택 - 스택 (백준 실버 4)
# 문제 링크: https://www.acmicpc.net/problem/10828

import sys
from collections import deque

def solution():
    data = sys.stdin.read().split()
    if not data: 
         return
    
    n = int(data[0])
    commands = data[1:]
    stack = []
    result = []

    ops = {
        "push": lambda x : stack.append(x),
        "pop": lambda: stack.pop() if stack else -1,
        "size":lambda: len(stack),
        "empty":lambda: 1 if not stack else 0,
        "top":lambda: stack[-1] if stack else -1
    }

    curr = 0
    while curr < len(commands):
        cmd = commands[curr]
        if cmd == "push":
            ops[cmd](commands[curr + 1])
            curr += 2
        else:
            result.append(str(ops[cmd]()))
            curr += 1

    sys.stdout.write("\n".join(result) + "\n")

if __name__ == "__main__":
    solution()