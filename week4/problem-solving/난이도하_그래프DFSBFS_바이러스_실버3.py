# 그래프, DFS, BFS - 바이러스 (백준 실버3)
# 문제 링크: https://www.acmicpc.net/problem/2606

import sys
from collections import deque

def solution():
    data = sys.stdin.read().split()
    n = int(data[0])
    c = int(data[1])
    graph = []

    for i in range(2, len(data), 2):
        graph.append((int(data[i]), int(data[i + 1])))

    visited = {1}
    que = deque([1])
    count = 0
    while que:
        curr = que.popleft()

        for u, v in graph:
            target = None
            if u == curr:
                target = v
            elif v == curr:
                target = u
            
            if target is not None and target not in visited:
                visited.add(target)
                que.append(target)
                count += 1        

    print(count)

solution()