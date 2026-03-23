# 트리 - 트리 만들기 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/14244

import sys
from collections import deque

def solution():
    data = sys.stdin.read().split()
    vertex = int(data[0])
    leaf = int(data[1])
    visited = [0]
    que = deque(0)
    count = 0
    result = {}
    for i in range(vertex):
        if count < m:
            visited.append((0, i))
            count += 1




solution()