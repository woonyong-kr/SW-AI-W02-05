"""
vizlib.grid
─────────────────────────────────────────────────────
Tile 과 Grid 클래스.

Tile
    - state      : 색상 팔레트 이름 ("unvisited", "visited", ...)
    - text       : 타일 위에 그릴 문자열 (짧은 라벨)
    - custom_color: state 색상을 무시하고 직접 RGB 지정

Grid
    - n x m 타일 배열
    - 상태 일괄 변경, 이웃 조회, 전체 리셋 등 헬퍼 제공
"""

from __future__ import annotations
from typing import Generator, Optional, Tuple, List


# ── 유효 상태 목록 ────────────────────────────────────────────────
VALID_STATES = frozenset({
    "unvisited", "visited", "frontier",
    "wall", "start", "end", "path",
})


class Tile:
    """그리드 한 칸."""

    __slots__ = ("row", "col", "state", "text", "_custom_color")

    def __init__(self, row: int, col: int) -> None:
        self.row   = row
        self.col   = col
        self.state = "unvisited"
        self.text  = ""
        self._custom_color: Optional[Tuple[int, int, int]] = None

    # ── 색상 제어 ─────────────────────────────────────────────────
    @property
    def custom_color(self) -> Optional[Tuple[int, int, int]]:
        return self._custom_color

    def set_color(self, color: Tuple[int, int, int]) -> None:
        """state 팔레트를 무시하고 직접 RGB 색상을 지정한다."""
        self._custom_color = tuple(color)

    def clear_color(self) -> None:
        """직접 지정한 색상을 해제하고 state 팔레트로 돌아간다."""
        self._custom_color = None

    def __repr__(self) -> str:
        return f"Tile({self.row},{self.col} state={self.state!r})"


class Grid:
    """n x m 타일 배열."""

    def __init__(self, rows: int, cols: int) -> None:
        self.rows  = rows
        self.cols  = cols
        self._tiles: list[list[Tile]] = [
            [Tile(r, c) for c in range(cols)]
            for r in range(rows)
        ]

    # ── 타일 접근 ─────────────────────────────────────────────────
    def get(self, row: int, col: int) -> Tile:
        return self._tiles[row][col]

    def __getitem__(self, pos: Tuple[int, int]) -> Tile:
        return self._tiles[pos[0]][pos[1]]

    def __iter__(self) -> Generator[Tile, None, None]:
        for row in self._tiles:
            yield from row

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    # ── 상태 변경 ─────────────────────────────────────────────────
    def set_state(self, row: int, col: int, state: str) -> None:
        """타일의 표시 상태를 변경한다."""
        if state not in VALID_STATES:
            raise ValueError(f"알 수 없는 state: {state!r}. "
                             f"허용값: {sorted(VALID_STATES)}")
        self._tiles[row][col].state = state

    def set_text(self, row: int, col: int, text) -> None:
        """타일 위에 그릴 짧은 라벨을 설정한다."""
        self._tiles[row][col].text = str(text)

    def set_color(self, row: int, col: int,
                  color: Tuple[int, int, int]) -> None:
        """state 팔레트를 우선시하지 않고 직접 RGB 색상을 지정한다."""
        self._tiles[row][col].set_color(color)

    def clear_color(self, row: int, col: int) -> None:
        self._tiles[row][col].clear_color()

    # ── 이웃 조회 ─────────────────────────────────────────────────
    def neighbors(
        self,
        row: int,
        col: int,
        diagonal: bool = False,
        include_walls: bool = False,
    ) -> List[Tuple[int, int]]:
        """
        (row, col) 의 이웃 좌표 목록을 반환한다.

        Parameters
        ----------
        diagonal     : True 이면 대각선 포함 (8방향)
        include_walls: False 이면 state=="wall" 인 타일 제외
        """
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if diagonal:
            dirs += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        result = []
        for dr, dc in dirs:
            nr, nc = row + dr, col + dc
            if not self.in_bounds(nr, nc):
                continue
            if not include_walls and self._tiles[nr][nc].state == "wall":
                continue
            result.append((nr, nc))
        return result

    # ── 전체 리셋 ─────────────────────────────────────────────────
    def reset(self) -> None:
        """모든 타일을 초기 상태로 되돌린다."""
        for tile in self:
            tile.state         = "unvisited"
            tile.text          = ""
            tile._custom_color = None

    def reset_path(self) -> None:
        """visited / frontier / path 만 초기화하고 wall / start / end 는 유지한다."""
        for tile in self:
            if tile.state in ("visited", "frontier", "path"):
                tile.state = "unvisited"
            tile.text          = ""
            tile._custom_color = None

    # ── 일괄 설정 ─────────────────────────────────────────────────
    def fill(self, state: str) -> None:
        """모든 타일의 state 를 동일하게 설정한다."""
        for tile in self:
            tile.state = state

    def set_wall_rect(
        self, r0: int, c0: int, r1: int, c1: int
    ) -> None:
        """(r0,c0) ~ (r1,c1) 직사각형 내부를 wall 로 채운다."""
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if self.in_bounds(r, c):
                    self._tiles[r][c].state = "wall"

    def count(self, state: str) -> int:
        """특정 state 인 타일 수를 반환한다."""
        return sum(1 for t in self if t.state == state)
