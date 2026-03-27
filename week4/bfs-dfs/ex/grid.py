"""
grid.py — 2D 격자 공용 유틸리티
============================================================
좌표계: (0,0) = 왼쪽 아래, (N-1,N-1) = 오른쪽 위
배열 접근: grid[N-1-y][x]

공개 함수:
    neighbors(grid, curr, N)         → 이동 가능한 이웃 목록
    move_cost(grid, src, dst, N)     → 이동 비용 (유클리드 + 가중치)
    print_grid(grid, N, *, path, start, goal)  → 격자 시각화
"""

import math

WALL = -99  # 통과 불가 셀 값

# 8방향 이동 (상하좌우 + 대각)
_DIRS = [
    ( 1,  0), (-1,  0), ( 0,  1), ( 0, -1),
    ( 1,  1), ( 1, -1), (-1,  1), (-1, -1),
]


def neighbors(grid, curr, N):
    """
    curr = (x, y) 기준으로 이동 가능한 이웃 셀 목록을 반환한다.
    - 격자 범위 밖이나 벽(-99)은 제외
    - 8방향 이동 지원
    """
    x, y = curr
    result = []
    for dx, dy in _DIRS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:
            if grid[N - 1 - ny][nx] != WALL:
                result.append((nx, ny))
    return result


def move_cost(grid, src, dst, N):
    """
    src → dst 이동 비용을 계산한다.
    공식: max(0.01, 유클리드거리 + 목적 셀 가중치)
    """
    base_dist = math.sqrt((src[0] - dst[0]) ** 2 + (src[1] - dst[1]) ** 2)
    weight    = grid[N - 1 - dst[1]][dst[0]]
    return max(0.01, base_dist + weight)


def print_grid(grid, N, *, path=None, start=None, goal=None):
    """
    격자를 텍스트로 출력한다.
    범례: S=출발  G=도착  *=경로  .=일반  ###=벽  +n/-n=가중치
    """
    path_set = set(path) if path else set()

    # 열 번호 헤더
    print("      " + "    ".join(str(x) for x in range(N)))
    print("    +" + "-----" * N)

    for row_idx in range(N):
        y    = N - 1 - row_idx   # 위(y=N-1)에서 아래(y=0)로 출력
        line = f" {y}  |"

        for x in range(N):
            cell = grid[N - 1 - y][x]
            pos  = (x, y)

            if pos == start and pos == goal:
                symbol = " SG "
            elif pos == start:
                symbol = "  S "
            elif pos == goal:
                symbol = "  G "
            elif cell == WALL:
                symbol = " ###"
            elif pos in path_set:
                symbol = "  * "
            elif cell > 0:
                symbol = f" +{cell} "
            elif cell < 0:
                symbol = f" {cell}"
            else:
                symbol = "  . "

            line += symbol + " "

        print(line)

    print()
