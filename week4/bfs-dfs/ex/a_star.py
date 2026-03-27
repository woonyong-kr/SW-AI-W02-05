"""
a_star.py — A* 최단 경로 (2D 격자 버전)
============================================================
좌표계: (0,0) = 왼쪽 아래, (N-1,N-1) = 오른쪽 위

g(n) = 시작점에서 n까지의 실제 누적 비용
h(n) = n에서 목표까지의 유클리드 거리  (허용 가능 휴리스틱)
f(n) = g(n) + h(n)

이동 비용 공식:
    base_dist = sqrt((x1-x2)^2 + (y1-y2)^2)   ← 유클리드 거리
    weight    = grid[(N-1-ny)][nx]              ← 목적 셀 가중치
    edge_cost = max(0.01, base_dist + weight)   ← 최솟값 보장
"""

import heapq
import math
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

def a_star(grid, start, goal, N):
    g_score   = {start: 0.0}
    came_from = {start: None}
    visited   = set()

    h_start = math.sqrt((start[0]-goal[0])**2 + (start[1]-goal[1])**2)
    pq      = [(h_start, 0.0, start)]   # (f, g, node)

    while pq:
        f_curr, g_curr, curr = heapq.heappop(pq)

        if curr in visited:
            continue
        visited.add(curr)

        if curr == goal:
            break

        for nb in neighbors(grid, curr, N):
            # ── 이동 비용 직접 계산 ──────────────────────
            base_dist = math.sqrt((curr[0]-nb[0])**2 + (curr[1]-nb[1])**2)
            weight    = grid[N-1-nb[1]][nb[0]]
            edge_cost = max(0.01, base_dist + weight)
            # ─────────────────────────────────────────────

            tentative_g = g_curr + edge_cost

            if tentative_g < g_score.get(nb, math.inf):
                g_score[nb]   = tentative_g
                came_from[nb] = curr

                # ── h(nb) ──────────────────────────────────
                h_nb = math.sqrt((nb[0]-goal[0])**2 + (nb[1]-goal[1])**2)
                # ─────────────────────────────────────────────
                f_nb = tentative_g + h_nb

                heapq.heappush(pq, (f_nb, tentative_g, nb))

    if goal not in came_from:
        return math.inf, []

    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return g_score[goal], path


# ── 실행 ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  A* 최단 경로 탐색 (2D 격자 유클리드 휴리스틱)")
    print("=" * 55)
    print(f"  시작: {START}  →  도착: {GOAL}")
    print("\n[맵]  S=출발  G=도착  .=일반  ###=벽  +n=추가비용  -n=감소비용")

    cost, path = a_star(GRID, START, GOAL, N)

    print_grid(GRID, N, path=path, start=START, goal=GOAL)

    if path:
        print(f"  최단 비용  : {cost:.4f}")
        print(f"  경로 길이  : {len(path)} 노드")
        print(f"  경로       : {' → '.join(str(p) for p in path)}")
        print()
        print("  [이동 단계별 비용]")
        for i in range(len(path) - 1):
            src, dst = path[i], path[i+1]
            base_dist = math.sqrt((src[0]-dst[0])**2 + (src[1]-dst[1])**2)
            weight    = GRID[N-1-dst[1]][dst[0]]
            edge_cost = max(0.01, base_dist + weight)
            print(f"    {src} → {dst}  유클리드={base_dist:.3f}  가중치={weight:+d}  비용={edge_cost:.3f}")
    else:
        print("  경로 없음")