"""
[A* 알고리즘 - 최단 경로 탐색]

문제 설명:
- 5×5 격자 맵에서 출발점(S)에서 도착점(G)까지의 최단 경로를 A*로 탐색합니다.
- '#'은 벽으로 이동할 수 없고, '.'은 이동 가능한 칸입니다.
- 한 번에 상/하/좌/우 4방향으로만 이동하며, 이동 1칸의 비용은 1입니다.

입력 (고정):
- 5×5 격자 GRID (0=이동가능, 1=벽)
- 시작: (0, 0) / 도착: (4, 4)

출력:
- 최단 경로 길이, 경로 좌표, 단계별 f/g/h 값

맵 시각화:
    S . . . .    ← row 0
    . # # . .    ← row 1  (벽: 1열, 2열)
    . . . . .    ← row 2
    . # . . .    ← row 3  (벽: 1열)
    . . . . G    ← row 4

예상 정답:
    최단 경로 길이: 8 칸
    경로: (0,0) → (0,1) → ... → (4,4)

──────────────────────────────────────────────────────────────
A* 알고리즘이란?
──────────────────────────────────────────────────────────────
- BFS의 업그레이드 버전: 방향성 있는 탐색으로 더 빠르게 목표 탐색
- 우선순위 큐(힙)로 f값이 가장 작은 노드부터 탐색

핵심 공식:
    f(n) = g(n) + h(n)
    │         │      └─ h(n): 현재→목표까지 예상 비용 [휴리스틱]
    │         └──────── g(n): 시작→현재까지 실제 누적 비용
    └────────────────── f(n): 총 예상 비용 (낮을수록 우선 탐색)

휴리스틱 (맨해튼 거리):
    h(a, b) = |a행 - b행| + |a열 - b열|
    예) h((1,2), (4,4)) = |1-4| + |2-4| = 3 + 2 = 5

허용 가능한 휴리스틱(Admissible):
    h(n) ≤ 실제 비용  →  A*가 항상 최단 경로를 보장!

탐색 순서:
    1. 우선순위 큐에서 f값이 가장 작은 노드 꺼내기
    2. 방문 처리 (중복 방문 방지)
    3. 목표 도달 시 종료
    4. 이웃 노드의 g, h, f 계산 → 큐에 추가

경로 역추적 (came_from 딕셔너리):
    도착점에서 출발점까지 came_from을 역순으로 따라가면 경로!
    goal → came_from[goal] → ... → start

BFS vs A* 비교:
    BFS:  모든 방향으로 균등하게 퍼져나감 (탐색 노드 ↑)
    A*:   목표 방향으로 집중 탐색 (탐색 노드 ↓, 효율적!)
"""

import heapq  # 우선순위 큐 (힙) 사용을 위한 모듈

# ── 맵 설정 (수정하지 마세요) ───────────────────────────────
# 0 = 이동 가능, 1 = 벽
GRID = [
    [0, 0, 0, 0, 0],  # row 0
    [0, 1, 1, 0, 0],  # row 1  ← 벽: (1,1), (1,2)
    [0, 0, 0, 0, 0],  # row 2
    [0, 1, 0, 0, 0],  # row 3  ← 벽: (3,1)
    [0, 0, 0, 0, 0],  # row 4
]

ROWS  = 5                  # 행 수
COLS  = 5                  # 열 수
START = (0, 0)             # 출발점 (row, col)
GOAL  = (4, 4)             # 도착점 (row, col)

# 4방향 이동: 위, 아래, 왼쪽, 오른쪽
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# ══════════════════════════════════════════════════════════════
# TODO 1: 휴리스틱 함수 구현
# ══════════════════════════════════════════════════════════════
def heuristic(a, b):
    """
    맨해튼 거리 휴리스틱을 계산합니다.

    A* 알고리즘에서 h(n)으로 사용됩니다.
    맨해튼 거리 = |행 차이| + |열 차이|

    Args:
        a: 현재 위치 (row, col)
        b: 목표 위치 (row, col)

    Returns:
        맨해튼 거리 (정수)

    예시:
        heuristic((0, 0), (4, 4)) → 8  (|0-4| + |0-4|)
        heuristic((1, 2), (4, 4)) → 5  (|1-4| + |2-4|)
    """
    # TODO: 행 차이의 절댓값과 열 차이의 절댓값을 더해서 반환하세요
    # 힌트: abs() 함수로 절댓값을 구합니다
    # 힌트: a와 b는 (row, col) 형태의 튜플입니다 → a[0]=행, a[1]=열
    pass  # ← 이 줄을 지우고 코드를 작성하세요


# ══════════════════════════════════════════════════════════════
# TODO 2: 이웃 노드 반환 함수 구현
# ══════════════════════════════════════════════════════════════
def get_neighbors(grid, node):
    """
    현재 노드에서 이동 가능한 이웃 노드 목록을 반환합니다.

    조건:
    1. 격자 범위 안에 있어야 함 (0 이상, ROWS/COLS 미만)
    2. 벽(grid값 == 1)이 아니어야 함

    Args:
        grid: 2D 격자 리스트
        node: 현재 위치 (row, col)

    Returns:
        이동 가능한 이웃 위치 리스트 [(row, col), ...]
    """
    row, col = node      # 현재 위치를 행(row)과 열(col)로 분리
    result = []          # 이동 가능한 이웃 목록

    for dr, dc in DIRECTIONS:       # 4방향(위/아래/왼/오른) 순서대로
        nr = row + dr               # 이웃의 행 위치
        nc = col + dc               # 이웃의 열 위치

        # TODO: 아래 두 가지 조건을 모두 만족하는 경우에만 result에 추가하세요
        # 조건 1: 격자 범위 안에 있어야 함
        #   → 0 <= nr < ROWS  이고  0 <= nc < COLS
        # 조건 2: 벽이 아니어야 함
        #   → grid[nr][nc] != 1

        # 힌트: if 문 하나로 두 조건을 'and'로 연결하세요
        # 힌트: result.append((nr, nc)) 로 추가합니다
        pass  # ← 이 줄을 지우고 코드를 작성하세요

    return result


# ══════════════════════════════════════════════════════════════
# TODO 3: A* 알고리즘 구현
# ══════════════════════════════════════════════════════════════
def a_star(grid, start, goal):
    """
    A* 알고리즘으로 start에서 goal까지 최단 경로를 찾습니다.

    핵심 자료구조:
        g_score   : {노드: 시작점에서 해당 노드까지의 실제 비용}
        came_from : {노드: 이전 노드} ← 경로 역추적에 사용
        visited   : 이미 처리된 노드 집합
        pq        : 우선순위 큐 [(f, g, 노드), ...]

    Args:
        grid : 2D 격자
        start: 출발점 (row, col)
        goal : 도착점 (row, col)

    Returns:
        (비용, 경로 리스트) 또는 (-1, []) 경로 없을 때
    """
    # ── 초기화 (수정하지 마세요) ────────────────────────────
    g_score   = {start: 0}      # 시작점의 g값 = 0
    came_from = {start: None}   # 시작점의 이전 노드 = 없음
    visited   = set()           # 방문한 노드 집합

    # 시작점의 f값 = g(0) + h(시작→목표)
    h_start = heuristic(start, goal)
    pq = [(h_start, 0, start)]  # (f, g, 노드) 형태로 큐에 삽입
    # ────────────────────────────────────────────────────────

    while pq:   # 큐가 빌 때까지 반복
        # TODO 3-1: 우선순위 큐에서 f값이 가장 작은 항목 꺼내기
        # 힌트: heapq.heappop(pq) → (f_curr, g_curr, curr) 형태
        # 힌트: f_curr=총예상비용, g_curr=실제누적비용, curr=현재노드
        pass  # ← 이 줄을 지우고 코드를 작성하세요

        # TODO 3-2: 이미 방문한 노드는 건너뛰기 (continue)
        # 힌트: if curr in visited: continue
        # 이유: 같은 노드가 큐에 여러 번 들어갈 수 있어서 체크 필요
        pass  # ← 이 줄을 지우고 코드를 작성하세요

        # TODO 3-3: 현재 노드를 방문 처리
        # 힌트: visited.add(curr)
        pass  # ← 이 줄을 지우고 코드를 작성하세요

        # TODO 3-4: 목표에 도달하면 탐색 종료 (break)
        # 힌트: if curr == goal: break
        pass  # ← 이 줄을 지우고 코드를 작성하세요

        # 이웃 노드 탐색 (수정하지 마세요)
        for neighbor in get_neighbors(grid, curr):

            # 이웃까지의 잠정 g값 = 현재 g값 + 이동 비용(1)
            tentative_g = g_curr + 1

            # TODO 3-5: 더 짧은 경로를 발견한 경우 업데이트
            # 조건: tentative_g < g_score.get(neighbor, float('inf'))
            # 수행할 작업:
            #   1) g_score[neighbor] = tentative_g       ← g값 갱신
            #   2) came_from[neighbor] = curr            ← 이전 노드 기록
            #   3) h = heuristic(neighbor, goal)         ← h값 계산
            #   4) f = tentative_g + h                   ← f = g + h
            #   5) heapq.heappush(pq, (f, tentative_g, neighbor))  ← 큐 추가
            pass  # ← 이 줄을 지우고 코드를 작성하세요

    # ── 경로 역추적 ─────────────────────────────────────────
    # goal이 came_from에 없으면 경로가 존재하지 않음
    if goal not in came_from:
        return -1, []

    # TODO 3-6: 경로 역추적 (goal → start 순서로 따라가기)
    # 힌트:
    #   path = []
    #   cur = goal
    #   while cur is not None:
    #       path.append(cur)
    #       cur = came_from[cur]   ← 이전 노드로 이동
    #   path.reverse()             ← start→goal 순서로 뒤집기
    pass  # ← 이 줄을 지우고 코드를 작성하세요

    # return g_score[goal], path   ← TODO 완료 후 이 주석을 해제하세요


# ── 시각화 함수 (수정하지 마세요) ────────────────────────────
def print_grid(grid, path=None, start=None, goal=None):
    """격자를 텍스트로 시각화"""
    path_set = set(path) if path else set()
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            pos = (r, c)
            if pos == start:
                row_str += "S "
            elif pos == goal:
                row_str += "G "
            elif pos in path_set:
                row_str += "* "
            elif grid[r][c] == 1:
                row_str += "# "
            else:
                row_str += ". "
        print(row_str.rstrip())


# ── 실행 (수정하지 마세요) ───────────────────────────────────
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

    cost, path = a_star(GRID, START, GOAL)

    if path:
        print("[결과]")
        print(f"  최단 경로 길이: {cost} 칸")
        print(f"  방문 노드 수  : {len(path)} 개")
        print(f"  경로: {' → '.join(str(p) for p in path)}")
        print()

        print("[경로 표시]  *=최단경로")
        print_grid(GRID, path=path, start=START, goal=GOAL)
        print()

        print("[이동 단계별 상세]")
        for i in range(len(path) - 1):
            src = path[i]
            dst = path[i + 1]
            h_val = heuristic(dst, GOAL)
            g_val = i + 1
            f_val = g_val + h_val
            print(f"  Step {i+1}: {src} → {dst}  | g={g_val}  h={h_val}  f={f_val}")
    else:
        print("[결과] 경로를 찾을 수 없습니다.")
