"""
vizlib.scene
─────────────────────────────────────────────────────
Scene : 알고리즘 시각화의 추상 기반 클래스.

파이프라인
----------
    define (setup)  →  solve (algorithm)  →  visualize (engine)

    1. setup()  : 자료구조 등록(use), 시작/종료 노드, HUD 범례
    2. solve()  : 알고리즘 로직 + visit/frontier/path 마킹 + yield
    3. Scene.run() : 엔진 생성 → 두 페이즈 setup → 제너레이터 루프

tile_shape 자동 결정
---------------------
use(struct) 호출 시 구조 타입을 보고 엔진에 자동 설정한다:
    NodeGraph / TreeNode  →  "circle"  (원형 노드, 그래프 느낌)
    Grid2D / Array1D      →  "rect"    (둥근 사각형, 격자 느낌)

solve() 에서 사용 가능한 메서드
--------------------------------
    타일 상태  : visit, frontier, path, wall, start, end, unvisit, mark
    타일 꾸미기: label(node, text),  color(node, rgb)
    이웃 탐색  : neighbors(node)
    HUD (선택) : info(key, value),  section(title)

자동 제공
---------
    Step 카운터  : yield 마다 HUD 의 "Step" 가 자동 갱신됨
    Wall 표시    : use(struct) 시 struct.wall_nodes() 자동 반영
    _start_node  : start(node) 호출 시 저장
    _end_node    : end(node) 호출 시 저장
"""

from __future__ import annotations

import abc
from typing import Any, Optional, Tuple

from .config import load_config
from .engine import Engine
from .grid   import Grid

_Struct = Any


class Scene(abc.ABC):
    """알고리즘 시각화 기반 클래스."""

    def __init__(self) -> None:
        self._struct:     Optional[_Struct] = None
        self._engine:     Optional[Engine]  = None
        self._start_node: Optional[Any]     = None
        self._end_node:   Optional[Any]     = None

    # ── 서브클래스 구현 ───────────────────────────────────────────────

    def setup(self) -> None:
        """
        자료구조·HUD 초기화.

        반드시 self.use(struct) 를 호출해 어댑터를 등록한다.
        self.start(node) / self.end(node) 로 특별 노드를 지정한다.
        HUD 섹션·범례는 setup() 안에만 작성한다.
        """

    @abc.abstractmethod
    def solve(self):
        """
        알고리즘을 작성한다.
        yield 로 한 스텝씩 렌더링을 분리한다.

        ✓  알고리즘 로직
        ✓  self.visit / frontier / path / wall / mark
        ✓  yield
        ✗  self.info  (Step 은 자동 카운트됨)
        """
        yield  # pragma: no cover

    # ── 자료구조 등록 ─────────────────────────────────────────────────

    def use(self, struct: _Struct) -> None:
        """
        자료구조 어댑터를 등록한다.

        - setup() 안에서 반드시 한 번 호출해야 한다.
        - struct 의 wall_nodes() 를 자동으로 'wall' 타일로 표시한다.
        - NodeGraph / TreeNode 이면 엔진의 tile_shape 을 "circle" 로 설정한다.
        """
        self._struct = struct

        # tile_shape 자동 결정
        if self._engine is not None:
            try:
                from .structures import NodeGraph
                self._engine._tile_shape = (
                    "circle" if isinstance(struct, NodeGraph) else "rect"
                )
            except ImportError:
                pass

        # 벽 자동 표시
        for node in struct.wall_nodes():
            self.wall(node)

    # ── 타일 상태 변경 ────────────────────────────────────────────────

    def mark(self, node: Any, state: str) -> None:
        if self._engine is None:
            return
        r, c = self._struct.to_tile(node)
        self._engine.grid.set_state(r, c, state)

    def visit(self, node: Any) -> None:
        self.mark(node, "visited")

    def frontier(self, node: Any) -> None:
        self.mark(node, "frontier")

    def path(self, node: Any) -> None:
        self.mark(node, "path")

    def wall(self, node: Any) -> None:
        self.mark(node, "wall")

    def start(self, node: Any) -> None:
        """start 상태로 표시하고 _start_node 에 저장한다."""
        self._start_node = node
        self.mark(node, "start")

    def end(self, node: Any) -> None:
        """end 상태로 표시하고 _end_node 에 저장한다."""
        self._end_node = node
        self.mark(node, "end")

    def unvisit(self, node: Any) -> None:
        self.mark(node, "unvisited")

    # ── 타일 꾸미기 ───────────────────────────────────────────────────

    def label(self, node: Any, text: Any) -> None:
        if self._engine is None:
            return
        r, c = self._struct.to_tile(node)
        self._engine.grid.set_text(r, c, text)

    def color(self, node: Any, rgb: Tuple[int, int, int]) -> None:
        if self._engine is None:
            return
        r, c = self._struct.to_tile(node)
        self._engine.grid.set_color(r, c, rgb)

    # ── 이웃 탐색 ─────────────────────────────────────────────────────

    def neighbors(self, node: Any) -> list:
        if self._struct is None:
            return []
        return self._struct.neighbors(node)

    # ── HUD ───────────────────────────────────────────────────────────

    def info(self, key: str, value: Any) -> None:
        """HUD 에 키-값 항목을 추가·갱신한다. setup() 에서 사용 권장."""
        if self._engine is None:
            return
        self._engine.hud.update(key, value)

    def section(self, title: str) -> None:
        """HUD 에 섹션 구분선을 추가한다. setup() 에서 사용 권장."""
        if self._engine is None:
            return
        self._engine.hud.section(title)

    # ── Tracer (옵저버) 재생 ──────────────────────────────────────────

    def replay(self, tracer: Any):
        """
        Tracer 에 기록된 이벤트를 애니메이션으로 재생(yield)한다.
        이를 통해 순수 알고리즘 로직과 시각화 렌더링을 완벽하게 분리할 수 있다.
        """
        for event in tracer.events:
            cmd = event[0]
            if cmd == "step":
                yield
            elif cmd == "visit":
                self.visit(event[1])
            elif cmd == "frontier":
                self.frontier(event[1])
            elif cmd == "path":
                self.path(event[1])
            elif cmd == "label":
                self.label(event[1], event[2])
            elif cmd == "color":
                self.color(event[1], event[2])
            elif cmd == "info":
                self.info(event[1], event[2])
            elif cmd == "start":
                self.start(event[1])
            elif cmd == "end":
                self.end(event[1])
            elif cmd == "unvisit":
                self.unvisit(event[1])

    # ── 실행 ──────────────────────────────────────────────────────────

    def run(
        self,
        title: Optional[str] = None,
        config_path: Optional[str] = None,
    ) -> None:
        """
        시각화를 시작한다.

        Parameters
        ----------
        title       : 창 제목 (None 이면 클래스 이름)
        config_path : vizlib.json 경로 (None 이면 기본값)
        """
        if title is None:
            title = type(self).__name__

        # ── Phase 1: 자료구조 크기 파악 (engine=None) ─────────────────
        self._engine = None
        self.setup()

        if self._struct is None:
            raise RuntimeError(
                "setup() 안에서 self.use(struct) 를 호출해 어댑터를 등록해야 합니다."
            )

        # ── Phase 2: 엔진 생성 ───────────────────────────────────────
        engine = Engine(title, config_path=config_path)
        engine.cfg["grid_rows"] = self._struct.tile_rows
        engine.cfg["grid_cols"] = self._struct.tile_cols
        engine.grid = Grid(self._struct.tile_rows, self._struct.tile_cols)
        
        # Grid 형태가 아니라면 빈 좌표는 투명하게 (숨김) 처리
        try:
            from .structures import Grid2D, Array1D
            is_grid = isinstance(self._struct, (Grid2D, Array1D))
        except ImportError:
            is_grid = True
            
        if not is_grid:
            for tile in engine.grid:
                tile.state = "hidden"
            for node in self._struct.all_nodes():
                # 등록된 실제 노드만 렌더링하도록 unvisited 마킹
                engine.grid.set_state(*self._struct.to_tile(node), "unvisited")

        # tile_shape 설정 (NodeGraph / TreeNode → circle)
        try:
            from .structures import NodeGraph
            engine._tile_shape = (
                "circle" if isinstance(self._struct, NodeGraph) else "rect"
            )
        except ImportError:
            pass

        # 엣지 정보 및 방향성 전달
        edges = self._struct.edges_as_tiles()
        if edges:
            engine._edges = edges
            engine._edges_directed = getattr(self._struct, "directed", False)

        self._engine = engine

        # ── 제너레이터 팩토리 ─────────────────────────────────────────
        scene_ref = self

        def _make_gen():
            scene_ref._engine.grid.reset()
            scene_ref._engine.hud.clear()
            scene_ref.setup()          # Phase 2: 타일 상태 + HUD 반영
            step = 0
            for _ in scene_ref.solve():
                step += 1
                scene_ref._engine.hud.update("Step", step)
                yield

        engine.set_loop(_make_gen(), reset_fn=_make_gen)
        engine.run()
