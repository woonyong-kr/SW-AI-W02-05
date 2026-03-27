"""
iddfs.py — 반복 심화 깊이 우선 탐색 (IDDFS, 2D 격자 버전)
============================================================
좌표계: (0,0) = 왼쪽 아래, (N-1,N-1) = 오른쪽 위
IDDFS는 가중치를 무시하고 최소 이동 횟수(홉 수)의 경로를 찾음
메모리 사용 O(d) — BFS에 비해 메모리 매우 적음
"""

import sys
from grid import neighbors, move_cost, print_grid

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

def dls(grid, curr, goal, N, depth_limit, visited, came_from):
    """깊이 제한 DFS (Depth-Limited Search) — IDDFS 내부 함수"""
    if curr == goal:
        return True
    if depth_limit == 0:
        return False

    visited.add(curr)
    for nb in neighbors(grid, curr, N):
        if nb not in visited:
            came_from[nb] = curr
            if dls(grid, nb, goal, N, depth_limit - 1, visited, came_from):
                return True
            del came_from[nb]
    visited.discard(curr)
    return False


def iddfs(grid, start, goal, N):
    """
    반복 심화 깊이 우선 탐색.
    반환: (최소 홉 수, 경로 좌표 리스트)
    """
    for limit in range(N * N):
        came_from = {start: None}
        visited   = set()
        if dls(grid, start, goal, N, limit, visited, came_from):
            path, cur = [], goal
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
            return limit, path
    return -1, []


# ── 실행 ───────────────────────────────────────────────────
if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    print("=" * 45)
    print("  반복 심화 DFS — IDDFS (2D 격자)")
    print("=" * 45)
    print(f"  시작: {START}  →  도착: {GOAL}")
    print("  ※ 가중치 무시 — 이동 횟수(홉) 최소화, 메모리 O(d)")
    print("\n[맵]  S=출발  G=도착  .=일반  ###=벽  +n=추가비용  -n=감소비용")

    hops, path = iddfs(GRID, START, GOAL, N)

    print_grid(GRID, N, path=path, start=START, goal=GOAL)

    if path:
        real_cost = sum(move_cost(GRID, path[i], path[i+1], N) for i in range(len(path)-1))
        print(f"  최소 홉 수 : {hops}")
        print(f"  실제 비용  : {real_cost:.4f}  (IDDFS는 비용 최적화 X)")
        print(f"  경로       : {' → '.join(str(p) for p in path)}")
    else:
        print("  경로 없음")