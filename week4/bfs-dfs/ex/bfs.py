"""
bfs.py — 너비 우선 탐색 (BFS, 2D 격자 버전)
============================================================
좌표계: (0,0) = 왼쪽 아래, (N-1,N-1) = 오른쪽 위
BFS는 가중치를 무시하고 최소 이동 횟수(홉 수)의 경로를 찾음
"""

import math
from collections import deque
from grid import neighbors, print_grid

# ── 샘플 맵 (5×5) ──────────────────────────────────────────
N = 5
GRID = [
    # y=4 (맨 위)
    [  0,   0,   0,   0,   0],
    [  0, -99, -99,   0,   0],   # y=3
    [  0,  +5,   0,  -3,   0],   # y=2
    [  0, -99,   0, -99,   0],   # y=1
    [  0,   0,   0,   0,   0],   # y=0 (맨 아래)
]

START = (0, 0)

GOAL  = (4, 4)

# ── 알고리즘 ───────────────────────────────────────────────

def bfs(grid, start, goal, N):
    visited   = {start}
    came_from = {start: None}
    queue     = deque([start])

    while queue:
        curr = queue.popleft()

        if curr == goal:
            break

        for nb in neighbors(grid, curr, N):
            if nb not in visited:
                visited.add(nb)
                came_from[nb] = curr
                queue.append(nb)

    if goal not in came_from:
        return -1, []

    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return len(path) - 1, path


# ── 실행 ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 45)
    print("  너비 우선 탐색 BFS (2D 격자)")
    print("=" * 45)
    print(f"  시작: {START}  →  도착: {GOAL}")
    print("  ※ 가중치 무시 — 이동 횟수(홉) 최소화")
    print("\n[맵]  S=출발  G=도착  .=일반  ###=벽  +n=추가비용  -n=감소비용")

    hops, path = bfs(GRID, START, GOAL, N)

    print_grid(GRID, N, path=path, start=START, goal=GOAL)

    if path:
        # 실제 비용 사후 계산 (인라인)
        total_cost = 0
        for i in range(len(path) - 1):
            src, dst = path[i], path[i+1]
            base_dist = math.sqrt((src[0]-dst[0])**2 + (src[1]-dst[1])**2)
            weight    = GRID[N-1-dst[1]][dst[0]]
            edge_cost = max(0.01, base_dist + weight)
            total_cost += edge_cost

        print(f"  최소 홉 수 : {hops}")
        print(f"  실제 비용  : {total_cost:.4f}  (BFS는 비용 최적화 X)")
        print(f"  경로       : {' → '.join(str(p) for p in path)}")
    else:
        print("  경로 없음")