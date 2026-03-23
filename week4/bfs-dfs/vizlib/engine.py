"""
vizlib.engine
─────────────────────────────────────────────────────
Engine : pygame 메인 루프, 그리드 렌더링, 이벤트 처리.

타일 크기 자동 계산
--------------------
config 의 tile_size = 0 이면 target_grid_w / target_grid_h 와
그리드 행·열 수로부터 tile_size 를 역산한다.
25×25 그리드는 작은 타일, 7×9 트리는 큰 타일이 되어
어떤 구조든 창 크기가 비슷하게 유지된다.

타일 모양
---------
engine._tile_shape = "rect"   → border_radius = tile_size // 6  (둥근 사각형)
engine._tile_shape = "circle" → border_radius = tile_size // 2  (원형)
Scene 이 NodeGraph / TreeNode 를 use() 할 때 자동으로 "circle" 로 설정한다.

키보드 단축키
-------------
    SPACE       : 일시정지 / 재개
    UP / DOWN   : 스텝 인터벌 ±20 ms (속도 조절)
    R           : 그리드 리셋 (알고리즘도 재시작)
    Q / ESC     : 종료
"""

from __future__ import annotations

import sys
import tracemalloc
from typing import Generator, Callable, Optional

import pygame

from .config import load_config, color

# ── SDL2 물리 키 스캔코드 (입력 모드·언어 무관) ─────────────────────
_SC_ESC   = 41
_SC_Q     = 20
_SC_R     = 21
_SC_SPACE = 44
_SC_UP    = 82
_SC_DOWN  = 81

from .grid import Grid
from .hud  import HUD, _load_font


class Engine:
    """vizlib 의 중심 클래스 — 창 관리, 렌더링, 이벤트, 스텝 실행."""

    def __init__(
        self,
        title: str = "vizlib",
        config_path: Optional[str] = None,
    ) -> None:
        self.cfg  = load_config(config_path)
        self.cfg["title"] = title

        rows = self.cfg["grid_rows"]
        cols = self.cfg["grid_cols"]

        self.grid = Grid(rows, cols)
        self.hud  = HUD(self.cfg)

        # ── 타일 모양 / 크기 (run() 에서 확정) ─────────────────────
        # "rect"   → 둥근 사각형  (Grid2D, Array1D)
        # "circle" → 원형         (NodeGraph, TreeNode)
        self._tile_shape: str = "rect"
        self._tile_size:  int = 0      # _init_pygame() 에서 계산

        # ── 루프 상태 ────────────────────────────────────────────────
        self._step_gen:    Optional[Generator]               = None
        self._reset_fn:    Optional[Callable[[], Generator]] = None
        self._interval_ms: int  = self.cfg["step_interval_ms"]
        self._last_step_t: int  = 0
        self._running:     bool = False
        self._paused:      bool = False
        self._done:        bool = False
        self._started:     bool = False   # R 키를 눌러야 True

        # ── NodeGraph / TreeNode 엣지 목록 ──────────────────────────
        self._edges: list = []

        # ── 메모리 추적 ──────────────────────────────────────────────
        self._track_mem: bool = False

        # ── pygame 오브젝트 (run() 이전은 None) ─────────────────────
        self._screen:    Optional[pygame.Surface]    = None
        self._clock:     Optional[pygame.time.Clock] = None
        self._font_tile: Optional[pygame.font.Font]  = None

        # ── 레이아웃 (run() 에서 계산) ──────────────────────────────
        self._grid_w = 0
        self._grid_h = 0
        self._win_w  = 0
        self._win_h  = 0

    # ── 공개 API ──────────────────────────────────────────────────────
    def set_loop(
        self,
        gen: Generator,
        reset_fn: Optional[Callable[[], Generator]] = None,
    ) -> None:
        self._step_gen  = gen
        self._reset_fn  = reset_fn
        self._done      = False

    def set_interval(self, ms: int) -> None:
        self._interval_ms = max(10, ms)
        self.cfg["step_interval_ms"] = self._interval_ms

    def enable_memory_tracking(self) -> None:
        self._track_mem = True
        tracemalloc.start()

    # ── 타일 크기 자동 계산 ───────────────────────────────────────────
    def _compute_tile_size(self) -> int:
        """
        target_grid_w / target_grid_h 에 맞게 타일 크기를 역산한다.

        공식: total_w = margin + cols * (size + margin)
              → size = (total_w - margin * (cols+1)) / cols
        """
        rows = self.grid.rows
        cols = self.grid.cols
        m    = self.cfg["tile_margin"]
        tw   = self.cfg["target_grid_w"]
        th   = self.cfg["target_grid_h"]
        smax = self.cfg["max_tile_size"]
        smin = self.cfg["min_tile_size"]

        s_w = (tw - m * (cols + 1)) // cols
        s_h = (th - m * (rows + 1)) // rows
        return max(smin, min(s_w, s_h, smax))

    # ── pygame 초기화 ──────────────────────────────────────────────────
    def _init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption(self.cfg["title"])

        # 창 크기 완전 고정 (고해상도 화질 보장)
        FIXED_W = 1200
        FIXED_H = 900
        hud_w   = 350
        grid_w  = FIXED_W - hud_w

        self.cfg["target_grid_w"] = grid_w
        self.cfg["target_grid_h"] = FIXED_H
        self.cfg["hud_width"] = hud_w

        cfg_s = self.cfg.get("tile_size", 0)
        s = int(cfg_s) if cfg_s and int(cfg_s) > 0 else self._compute_tile_size()
        self._tile_size = s

        self._grid_w = grid_w
        self._grid_h = FIXED_H
        self._win_w  = FIXED_W
        self._win_h  = FIXED_H

        # SCALED를 주어 맥북 레티나 화질 깨짐을 극복합니다.
        self._screen = pygame.display.set_mode(
            (self._win_w, self._win_h),
            pygame.SCALED | pygame.RESIZABLE
        )
        self._clock     = pygame.time.Clock()
        
        # 글꼴 크기를 크게 잡아 해상도를 높입니다.
        self._font_tile = _load_font(max(12, s // 2))

        pygame.key.stop_text_input()
        self._glow_cache = {}

    def _draw_glow(self, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]) -> None:
        """반투명 원을 여러 겹 겹쳐 그려 네온사인 글로우(Glow) 효과를 냅니다."""
        key = (radius, tuple(color[:3]))
        if key not in self._glow_cache:
            surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            for i in range(3, 0, -1):
                r = radius + i * max(2, radius // 2)
                alpha = 80 // i
                pygame.draw.circle(surf, (*color[:3], alpha), (radius * 2, radius * 2), r)
            self._glow_cache[key] = surf
        surf = self._glow_cache[key]
        self._screen.blit(surf, (center[0] - radius * 2, center[1] - radius * 2))

    # ── 렌더링 ────────────────────────────────────────────────────────
    _STATE_TO_COLOR_KEY = {
        "unvisited": "unvisited",
        "visited":   "visited",
        "frontier":  "frontier",
        "wall":      "wall",
        "start":     "start",
        "end":       "end",
        "path":      "path",
    }

    def _tile_color(self, tile) -> tuple:
        if tile.custom_color:
            return tile.custom_color
        return color(self.cfg, self._STATE_TO_COLOR_KEY.get(tile.state, "unvisited"))

    def _tile_rect(self, row: int, col: int) -> pygame.Rect:
        s = self._tile_size
        m = self.cfg["tile_margin"]
        
        # 고정된 캔버스 중앙에 타일을 정렬하기 위한 offset 계산
        cols = self.grid.cols
        rows = self.grid.rows
        content_w = cols * s + (cols + 1) * m
        content_h = rows * s + (rows + 1) * m
        
        offset_x = max(0, (self._grid_w - content_w) // 2)
        offset_y = max(0, (self._grid_h - content_h) // 2)

        x = offset_x + m + col * (s + m)
        y = offset_y + m + row * (s + m)
        return pygame.Rect(x, y, s, s)

    def _tile_radius(self) -> int:
        """tile_shape 에 따라 border_radius 를 반환한다."""
        s = self._tile_size
        if self._tile_shape == "circle":
            return s // 2
        return max(2, s // 6)

    def _draw(self) -> None:
        self._screen.fill(color(self.cfg, "background"))

        s = self._tile_size
        r = self._tile_radius()

        # ── NodeGraph / TreeNode 엣지 ────────────────────────────────
        if self._edges:
            edge_col = (80, 95, 130) # 선 색깔을 좀 더 세련되게 바꿈
            directed = getattr(self, "_edges_directed", False)
            import math
            for (r1, c1), (r2, c2) in self._edges:
                p1 = self._tile_rect(r1, c1).center
                p2 = self._tile_rect(r2, c2).center
                thickness = max(2, s // 15)
                pygame.draw.line(self._screen, edge_col, p1, p2, thickness)
                
                # '단방향' 그래프일 경우 종점(화살촉)을 예쁘게 그립니다.
                if directed:
                    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
                    angle = math.atan2(dy, dx)
                    # p2 중앙에서 노드 반지름만큼 후퇴하여 '원 테두리'에 화살표가 붙게 함
                    node_radius = s // 2 + thickness
                    cx = p2[0] - math.cos(angle) * node_radius
                    cy = p2[1] - math.sin(angle) * node_radius
                    
                    head_size = max(6, s // 4)
                    pt1 = (cx, cy)
                    pt2 = (cx - math.cos(angle - 0.5) * head_size, cy - math.sin(angle - 0.5) * head_size)
                    pt3 = (cx - math.cos(angle + 0.5) * head_size, cy - math.sin(angle + 0.5) * head_size)
                    
                    # 화살촉 폴리곤 렌더링
                    pygame.draw.polygon(self._screen, (120, 160, 230), [pt1, pt2, pt3])

        # ── 타일 ─────────────────────────────────────────────────────
        for tile in self.grid:
            # 빈 노드(숨김 처리된 좌표)는 아예 렌더링하지 않아 여백처럼 보이게 합니다!
            if tile.state == "hidden":
                continue
                
            rect   = self._tile_rect(tile.row, tile.col)
            tcolor = self._tile_color(tile)
            
            # Glow 효과 추가 (네온사인 렌더링)
            if tile.state in ("start", "end", "path", "frontier"):
                self._draw_glow(rect.center, max(4, s // 2), tcolor)
                
            pygame.draw.rect(self._screen, tcolor, rect, border_radius=r)

            # start / end / path 중앙 강조 포인트
            if tile.state == "start":
                pygame.draw.circle(
                    self._screen, (255, 255, 255),
                    rect.center, max(3, s // 4),
                )
            elif tile.state == "end":
                pygame.draw.circle(
                    self._screen, (255, 255, 255),
                    rect.center, max(3, s // 4),
                )
            elif tile.state == "path":
                pygame.draw.circle(
                    self._screen, (255, 255, 255),
                    rect.center, max(2, s // 5),
                )

            # 라벨 텍스트
            if tile.text:
                surf = self._font_tile.render(
                    tile.text, True, color(self.cfg, "text_tile")
                )
                tx = rect.x + (rect.width  - surf.get_width())  // 2
                ty = rect.y + (rect.height - surf.get_height()) // 2
                self._screen.blit(surf, (tx, ty))

        # ── HUD ───────────────────────────────────────────────────────
        self.hud.draw(
            self._screen,
            self._grid_w, 0,
            self.cfg["hud_width"], self._win_h,
        )

        # ── 시작 전 오버레이 ─────────────────────────────────────────
        if not self._started:
            self._draw_start_overlay()

        pygame.display.flip()

    def _draw_start_overlay(self) -> None:
        overlay = pygame.Surface((self._grid_w, self._grid_h), pygame.SRCALPHA)
        overlay.fill((8, 10, 18, 200))
        self._screen.blit(overlay, (0, 0))

        f_big = _load_font(24)
        f_sub = _load_font(13)
        cx = self._grid_w // 2
        cy = self._grid_h // 2

        box_w, box_h = 280, 90
        bx, by = cx - box_w // 2, cy - box_h // 2
        box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box.fill((25, 28, 48, 230))
        self._screen.blit(box, (bx, by))
        pygame.draw.rect(
            self._screen, (60, 80, 160),
            (bx, by, box_w, box_h), 1, border_radius=6,
        )

        l1 = f_big.render("R  키를 눌러 시작", True, (200, 220, 255))
        l2 = f_sub.render("창을 클릭한 뒤 R을 누르세요", True, (100, 115, 160))
        self._screen.blit(l1, (cx - l1.get_width() // 2, by + 14))
        self._screen.blit(l2, (cx - l2.get_width() // 2, by + 55))

    # ── 스텝 실행 ─────────────────────────────────────────────────────
    def _try_step(self) -> None:
        if self._step_gen is None or self._done or self._paused or not self._started:
            return
        now = pygame.time.get_ticks()
        if now - self._last_step_t < self._interval_ms:
            return
        self._last_step_t = now
        try:
            next(self._step_gen)
            if self._track_mem:
                cur, peak = tracemalloc.get_traced_memory()
                self.hud.update("Mem current", f"{cur / 1024:.1f} KB")
                self.hud.update("Mem peak",    f"{peak / 1024:.1f} KB")
        except StopIteration:
            self._done = True
            self.hud.update("Status", "Done")

    # ── 이벤트 처리 ───────────────────────────────────────────────────
    def _handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self._running = False

        elif event.type == pygame.KEYDOWN:
            sc = event.scancode

            if sc in (_SC_Q, _SC_ESC):
                self._running = False

            elif sc == _SC_SPACE:
                self._paused = not self._paused
                self.hud.update("Status", "Paused" if self._paused else "Running")

            elif sc == _SC_R:
                self.grid.reset()
                self._done    = False
                self._paused  = False
                self._started = True
                if self._reset_fn:
                    self._step_gen = self._reset_fn()
                self.hud.update("Status", "Running")

            elif sc == _SC_UP:
                self._interval_ms = max(10, self._interval_ms - 20)
                self.hud.update("Speed", f"{self._interval_ms} ms/step")

            elif sc == _SC_DOWN:
                self._interval_ms = min(3000, self._interval_ms + 20)
                self.hud.update("Speed", f"{self._interval_ms} ms/step")

    # ── 메인 루프 ─────────────────────────────────────────────────────
    def run(self) -> None:
        self._init_pygame()

        s = self._tile_size
        self.hud.update("Status", "R 키를 눌러 시작")
        self.hud.update("Speed",  f"{self._interval_ms} ms/step")
        self.hud.update("Grid",   f"{self.grid.rows} × {self.grid.cols}  ({s}px)")

        self._running = True
        while self._running:
            for event in pygame.event.get():
                self._handle_event(event)
            self._try_step()
            self._draw()
            self._clock.tick(self.cfg["fps"])

        pygame.quit()
