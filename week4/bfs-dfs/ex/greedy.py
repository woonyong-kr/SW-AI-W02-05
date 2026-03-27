"""
greedy.py — 탐욕 최우선 탐색 (Greedy Best-First, 2D 격자 버전)
============================================================
좌표계: (0,0) = 왼쪽 아래, (N-1,N-1) = 오른쪽 위

휴리스틱 h(n) = euclidean(n, goal)  — 실제 비용은 무시
탐욕 탐색은 최단 경로를 보장하지 않음
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

def greedy_best_first(grid, start, goal, N):
    visited   = set()
    came_from = {start: None}

    # 우선순위 = h(n) = 목표까지 유클리드 거리
    h_start = math.sqrt((start[0]-goal[0])**2 + (start[1]-goal[1])**2)
    pq      = [(h_start, start)]

    while pq:
        _, curr = heapq.heappop(pq)

        if curr == goal:
            break

        if curr in visited:
            continue
        visited.add(curr)

        for nb in neighbors(grid, curr, N):
            if nb not in visited and nb not in came_from:
                came_from[nb] = curr

                # ── h(nb): 이웃에서 목표까지 유클리드 ──────
                h_nb = math.sqrt((nb[0]-goal[0])**2 + (nb[1]-goal[1])**2)
                # ─────────────────────────────────────────────

                heapq.heappush(pq, (h_nb, nb))

    if goal not in came_from:
        return False, []

    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return True, path


# ── 실행 ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 45)
    print("  탐욕 최우선 탐색 (Greedy Best-First Search)")
    print("=" * 45)
    print(f"  시작: {START}  →  도착: {GOAL}")
    print("  ※ h(n)=유클리드거리만 보기 때문에 최단 경로 미보장")
    print("\n[맵]  S=출발  G=도착  .=일반  ###=벽  +n=추가비용  -n=감소비용")

    found, path = greedy_best_first(GRID, START, GOAL, N)

    print_grid(GRID, N, path=path, start=START, goal=GOAL)

    if found:
        print(f"  도달 성공!")
        print(f"  경로 길이  : {len(path)} 노드")
        print(f"  경로       : {' → '.join(str(p) for p in path)}")
        print()
        print("  [단계별 h값 / 실제 이동 비용]")
        total_cost = 0
        for i in range(len(path) - 1):
            src, dst = path[i], path[i+1]
            h_val     = math.sqrt((dst[0]-GOAL[0])**2 + (dst[1]-GOAL[1])**2)
            base_dist = math.sqrt((src[0]-dst[0])**2 + (src[1]-dst[1])**2)
            weight    = GRID[N-1-dst[1]][dst[0]]
            edge_cost = max(0.01, base_dist + weight)
            total_cost += edge_cost
            print(f"    {src} → {dst}  h={h_val:.3f}  유클리드={base_dist:.3f}  가중치={weight:+d}  비용={edge_cost:.3f}")
        print(f"\n  실제 총 비용 : {total_cost:.4f}  (탐욕 탐색이 최적 아닐 수 있음)")
    else:
        print("  경로 없음")