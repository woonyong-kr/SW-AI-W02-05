import heapq  # 우선순위 큐 (힙) 사용을 위한 모듈

# ── 맵 설정 ───────────────────────────────────────────────
GRID = [
    [0, 0, 0, 0, 0],  # row 0
    [0, 1, 1, 0, 0],  # row 1
    [0, 0, 0, 0, 0],  # row 2
    [0, 1, 0, 0, 0],  # row 3
    [0, 0, 0, 0, 0],  # row 4
]

ROWS  = 5
COLS  = 5
START = (0, 0)
GOAL  = (4, 4)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# ══════════════════════════════════════════════════════════════
# TODO 1: 휴리스틱 함수 구현 (완성)
# ══════════════════════════════════════════════════════════════
def heuristic(a, b):
    # 맨해튼 거리 = |행 차이| + |열 차이|
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ══════════════════════════════════════════════════════════════
# TODO 2: 이웃 노드 반환 함수 구현 (완성)
# ══════════════════════════════════════════════════════════════
def get_neighbors(grid, node):
    row, col = node
    result = []

    for dr, dc in DIRECTIONS:
        nr, nc = row + dr, col + dc
        # 격자 범위 내에 있고, 벽(1)이 아닌 경우만 추가
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] != 1:
            result.append((nr, nc))
    return result

# ══════════════════════════════════════════════════════════════
# TODO 3: A* 알고리즘 구현 (완성)
# ══════════════════════════════════════════════════════════════
def a_star(grid, start, goal):
    g_score   = {start: 0}      
    came_from = {start: None}   
    visited   = set()           

    h_start = heuristic(start, goal)
    pq = [(h_start, 0, start)]  # (f, g, node)

    while pq:
        # TODO 3-1: f값이 가장 작은 항목 꺼내기
        f_curr, g_curr, curr = heapq.heappop(pq)

        # TODO 3-2: 이미 방문한 노드는 건너뛰기
        if curr in visited:
            continue

        # TODO 3-3: 현재 노드를 방문 처리
        visited.add(curr)

        # TODO 3-4: 목표에 도달하면 탐색 종료
        if curr == goal:
            break

        for neighbor in get_neighbors(grid, curr):
            tentative_g = g_curr + 1

            # TODO 3-5: 더 짧은 경로를 발견한 경우 업데이트
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                came_from[neighbor] = curr
                h = heuristic(neighbor, goal)
                f = tentative_g + h
                heapq.heappush(pq, (f, tentative_g, neighbor))

    if goal not in came_from:
        return -1, [], 0, {}

    # TODO 3-6: 경로 역추적 (goal -> start)
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    return g_score[goal], path, len(path), g_score

# ── 시각화 함수 ───────────────────────────────────────────
def print_grid(grid, path=None, start=None, goal=None):
    path_set = set(path) if path else set()
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            pos = (r, c)
            if pos == start: row_str += "S "
            elif pos == goal: row_str += "G "
            elif pos in path_set: row_str += "* "
            elif grid[r][c] == 1: row_str += "# "
            else: row_str += ". "
        print(row_str.rstrip())

# ── 실행부 ────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== A* 최단 경로 탐색 ===")
    print()
    print("[초기 맵]  S=출발  G=도착  #=벽  .=이동가능")
    print_grid(GRID, start=START, goal=GOAL)
    print()
    print("[A* 탐색 시작]")
    print(f"  출발: {START}")
    print(f"  도착: {GOAL}")
    print()

    cost, path, visited_count, g_score = a_star(GRID, START, GOAL)

    if path:
        print(f"[결과]")
        print(f"  최단 경로 길이: {cost} 칸")
        print(f"  방문 노드 수  : {visited_count} 개")
        print(f"  경로: {' → '.join(str(p) for p in path)}")
        print()
        print("[경로 표시]  *=최단경로")
        print_grid(GRID, path=path, start=START, goal=GOAL)
        print()
        print("[이동 단계별 상세]")
        for i in range(1, len(path)):
            prev = path[i - 1]
            curr = path[i]
            g = g_score[curr]
            h = heuristic(curr, GOAL)
            f = g + h
            print(f"  Step {i}: {prev} → {curr}  | g={g}  h={h}  f={f}")
    else:
        print("경로를 찾을 수 없습니다.")