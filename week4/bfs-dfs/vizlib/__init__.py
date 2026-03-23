"""
vizlib — pygame 기반 알고리즘 시각화 라이브러리
=================================================

권장 사용 방법 (Scene API)
--------------------------
    from vizlib import Scene, Grid2D

    class MyAlgorithm(Scene):
        def setup(self):
            self.use(Grid2D(20, 20))
            self.start((0, 0))
            self.end((19, 19))

        def solve(self):
            # 알고리즘 코드만 작성
            self.visit((0, 0))
            yield

    MyAlgorithm().run("내 알고리즘", config_path="vizlib.json")

저수준 API (직접 엔진 사용)
----------------------------
    from vizlib import Engine

    eng  = Engine("My Demo", config_path="vizlib.json")
    grid = eng.grid
    hud  = eng.hud

    def algorithm():
        grid.set_state(0, 0, "visited")
        hud.update("Step", 1)
        yield

    eng.set_loop(algorithm())
    eng.run()
"""

from .engine     import Engine
from .grid       import Grid, Tile, VALID_STATES
from .hud        import HUD
from .config     import load_config, DEFAULTS, color
from .scene      import Scene
from .structures import Structure, Grid2D, Array1D, NodeGraph, TreeNode

__all__ = [
    # Scene API  ← 여기서부터 사용
    "Scene",
    "Structure",   # 커스텀 자료구조 기반 클래스
    "Grid2D",      # 2차원 격자 (벽 지원)
    "Array1D",     # 1차원 배열 (wrap_cols 지원)
    "NodeGraph",   # 임의 노드+엣지 그래프
    "TreeNode",    # 트리 (BFS 레벨 자동 레이아웃)
    # 저수준 API  ← 엔진을 직접 다룰 때
    "Engine",
    "Grid",
    "Tile",
    "HUD",
    "VALID_STATES",
    "load_config",
    "DEFAULTS",
    "color",
]
