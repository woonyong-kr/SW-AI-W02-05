# 그래프, DFS, BFS - 점프왕 쩰리 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/16173

import sys
from collections import deque

def solution():
    data = sys.stdin.read().split()
    n = int(data[0])
    grid = []

    for i in range(n):
        grid.append(list(map(int, data[(i * n + 1):(i + 1) * n + 1])))

    def dfs(grid, node, visited):
        row, col = node

        if row >= n or col >= n or (row, col) in visited:
            return False

        visited.add((row, col))

        if grid[row][col] == -1:
            return True

        mov = grid[row][col]

        if mov == 0:
            return False
        if row + mov <= n - 1:
            if dfs(grid, (row + mov, col), visited):
                return True
        if col + mov <= n - 1:
            if dfs(grid, (row, col + mov), visited):
                return True

        return False

    print("HaruHaru") if dfs(grid, (0, 0), set()) else print("Hing")

def solution2():
    data = sys.stdin.read().split()
    n = int(data[0])
    grid = []

    for i in range(n):
        grid.append(list(map(int, data[(i * n + 1):(i + 1) * n + 1])))

    visited = set()
    que = deque([(0, 0)])

    while que:
        row, col = que.popleft()

        if row >= n or col >= n or (row, col) in visited:
            continue

        visited.add((row, col))

        if grid[row][col] == -1:
            print("HaruHaru")
            return
        
        mov = grid[row][col]

        if mov == 0:
            continue
        if row + mov <= n - 1:
            que.append((row + mov, col))
        if col + mov <= n - 1:
            que.append((row, col + mov))

    
    print("Hing")

solution()