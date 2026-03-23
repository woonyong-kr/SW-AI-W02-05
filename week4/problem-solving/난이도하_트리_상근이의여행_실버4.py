# 트리 - 상근이의 여행 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/9372

import sys
from collections import deque

def solution():
    data = sys.stdin.read().split()
    ptr = 0
    case = int(data[ptr])
    ptr += 1
    for _ in range(case):
        n = int(data[ptr])
        m = int(data[ptr + 1])
        ptr += 2
        graph = [[] for _ in range(n + 1)]
        for _ in range(m):
            u = int(data[ptr])
            v = int(data[ptr + 1])
            graph[u].append(v)
            graph[v].append(u)
            ptr += 2

        visited = [False] * (n + 1)
        visited[1] = True
        que = deque([1])
        count = 0

        while que:
            for val in graph[que.popleft()]:
                if not visited[val]:
                    visited[val] = True
                    que.append(val)
                    count += 1

        print(count)

def solution2():  
    data = sys.stdin.read().split()
    ptr = 0
    case = int(data[ptr])
    ptr += 1
    for _ in range(case):
        n = int(data[ptr])
        m = int(data[ptr + 1])
        print(n - 1)
        ptr += 2 + (2 * m)

solution2()