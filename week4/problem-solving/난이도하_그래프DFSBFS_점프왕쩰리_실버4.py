# 그래프, DFS, BFS - 점프왕 쩰리 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/16173

import sys

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

        visited.append((row, col))

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

    print("HaruHaru") if dfs(grid, (0, 0), []) else print("Hing")
    
solution()