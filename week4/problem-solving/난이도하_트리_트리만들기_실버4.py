# 트리 - 트리 만들기 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/14244

import sys
from collections import deque

def solution():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])

    result = []
    cont = 0
    for i in range(1, n):
        if i <= m:
            result.append((0, i))
            count = i
        else:
            result.append((count, i))
            count = i
    
    for edge in result:
        print(f"{edge[0]} {edge[1]}")


# 0 1 
# 0 2
# 0 3
# 3 4
# 4 5

solution()