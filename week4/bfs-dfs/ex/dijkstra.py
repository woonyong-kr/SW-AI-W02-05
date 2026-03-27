"""
dijkstra.py — 다익스트라 최단 경로 (2D 격자 버전)
============================================================
좌표계: (0,0) = 왼쪽 아래, (N-1,N-1) = 오른쪽 위

이동 비용 공식 (인라인):
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

def dijkstra(grid, start, goal, N):
    dist      = {start: 0.0}
    came_from = {start: None}
    pq        = [(0.0, start)]

    while pq:
        curr_dist, curr = heapq.heappop(pq)

        if curr == goal:
            break

        if curr_dist > dist.get(curr, math.inf):
            continue

        for nb in neighbors(grid, curr, N):
            # ── 이동 비용 직접 계산 ──────────────────────
            base_dist = math.sqrt((curr[0]-nb[0])**2 + (curr[1]-nb[1])**2)
            weight    = grid[N-1-nb[1]][nb[0]]          # 목적 셀 가중치
            edge_cost = max(0.01, base_dist + weight)   # 음수 방지
            # ─────────────────────────────────────────────

            new_dist = curr_dist + edge_cost
            if new_dist < dist.get(nb, math.inf):
                dist[nb]      = new_dist
                came_from[nb] = curr
                heapq.heappush(pq, (new_dist, nb))

    if goal not in came_from:
        return math.inf, []

    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return dist[goal], path


# ── 실행 ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 45)
    print("  다익스트라 최단 경로 (2D 격자 유클리드)")
    print("=" * 45)
    print(f"  시작: {START}  →  도착: {GOAL}")
    print("\n[맵]  S=출발  G=도착  .=일반  ###=벽  +n=추가비용  -n=감소비용")

    cost, path = dijkstra(GRID, START, GOAL, N)

    print_grid(GRID, N, path=path, start=START, goal=GOAL)

    if path:
        print(f"  최단 비용 : {cost:.4f}")
        print(f"  경로 길이 : {len(path)} 노드")
        print(f"  경로      : {' → '.join(str(p) for p in path)}")
        print()
        print("  [단계별 이동 비용]")
        for i in range(len(path) - 1):
            src, dst = path[i], path[i+1]
            base_dist = math.sqrt((src[0]-dst[0])**2 + (src[1]-dst[1])**2)
            weight    = GRID[N-1-dst[1]][dst[0]]
            edge_cost = max(0.01, base_dist + weight)
            print(f"    {src} → {dst}  유클리드={base_dist:.3f}  가중치={weight:+d}  비용={edge_cost:.3f}")
    else:
        print("  경로 없음")