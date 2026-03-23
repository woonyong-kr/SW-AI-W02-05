"""
vizlib.structures
─────────────────────────────────────────────────────
자료구조 어댑터 — "노드" 를 타일 (row, col) 로 변환하는 통합 인터페이스.

핵심 개념
---------
모든 자료구조는 결국 **노드 + 엣지** 그래프다.
"어디에 그릴지(tile 좌표)"와 "무엇이 이웃인지(neighbors)" 만 정의하면
어떤 구조든 동일한 시각화 파이프라인을 통과한다.

    Array1D   → 노드: 정수 인덱스  / 레이아웃: 가로 한 줄 (or wrap)
    Grid2D    → 노드: (row, col)   / 레이아웃: 격자 (동일 매핑)
    NodeGraph → 노드: 임의 값      / 레이아웃: 직접 지정
    TreeNode  → 노드: 임의 값      / 레이아웃: 자동 BFS 레벨 트리

커스텀 자료구조 만들기
----------------------
Structure 를 상속하고 추상 멤버 5개를 구현한다:

    class MyStruct(Structure):
        @property
        def tile_rows(self): return ...
        @property
        def tile_cols(self): return ...
        def to_tile(self, node): return (row, col)
        def neighbors(self, node): return [...]
        def all_nodes(self): return [...]

선택적 오버라이드
-----------------
    wall_nodes()       → 벽/장애물 노드 목록  (Scene 이 자동 표시)
    edges_as_tiles()   → 엣지 타일 좌표 쌍    (NodeGraph / TreeNode 전용)
"""

from __future__ import annotations

import abc
import math
from collections import deque
from typing import Any, Dict, List, Optional, Set, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# Structure  — 추상 기반 클래스
# ─────────────────────────────────────────────────────────────────────────────

class Structure(abc.ABC):
    """
    모든 자료구조 어댑터의 공통 인터페이스.
    서브클래스는 tile_rows, tile_cols, to_tile, neighbors, all_nodes 를 구현한다.
    """

    @property
    @abc.abstractmethod
    def tile_rows(self) -> int:
        """그리드 총 행 수."""

    @property
    @abc.abstractmethod
    def tile_cols(self) -> int:
        """그리드 총 열 수."""

    @abc.abstractmethod
    def to_tile(self, node: Any) -> Tuple[int, int]:
        """노드 → (row, col) 타일 좌표."""

    @abc.abstractmethod
    def neighbors(self, node: Any) -> List[Any]:
        """인접 노드 목록."""

    @abc.abstractmethod
    def all_nodes(self) -> List[Any]:
        """모든 노드 목록."""

    def wall_nodes(self) -> List[Any]:
        """벽/장애물 노드 목록. Scene.use() 에서 자동으로 'wall' 타일로 표시된다."""
        return []

    def edges_as_tiles(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """엣지를 타일 좌표 쌍 목록으로 반환. NodeGraph/TreeNode 렌더링에 사용."""
        return []


# ─────────────────────────────────────────────────────────────────────────────
# Array1D
# ─────────────────────────────────────────────────────────────────────────────

class Array1D(Structure):
    """
    1차원 배열 어댑터.

    노드: 정수 인덱스 (0 ~ size-1)
    레이아웃: row=0, col=index (단일 행)
              wrap_cols 를 지정하면 다중 행으로 표시

    예시
    ----
        a = Array1D(10)           # 0~9, 1행 10열
        a = Array1D(20, wrap_cols=5)  # 0~19, 4행 5열
    """

    def __init__(self, size: int, wrap_cols: Optional[int] = None) -> None:
        self.size      = size
        self.wrap_cols = wrap_cols

    @property
    def tile_rows(self) -> int:
        return math.ceil(self.size / self.wrap_cols) if self.wrap_cols else 1

    @property
    def tile_cols(self) -> int:
        return self.wrap_cols if self.wrap_cols else self.size

    def to_tile(self, node: int) -> Tuple[int, int]:
        return divmod(node, self.wrap_cols) if self.wrap_cols else (0, node)

    def neighbors(self, node: int) -> List[int]:
        """인접 인덱스 (왼쪽·오른쪽). wrap_cols 경계는 넘지 않는다."""
        result = []
        if node > 0:
            result.append(node - 1)
        if node < self.size - 1:
            result.append(node + 1)
        return result

    def all_nodes(self) -> List[int]:
        return list(range(self.size))

    def __repr__(self) -> str:
        if self.wrap_cols:
            return f"Array1D(size={self.size}, wrap_cols={self.wrap_cols})"
        return f"Array1D(size={self.size})"


# ─────────────────────────────────────────────────────────────────────────────
# Grid2D
# ─────────────────────────────────────────────────────────────────────────────

class Grid2D(Structure):
    """
    2차원 격자 어댑터.

    노드: (row, col) 정수 튜플
    레이아웃: 동일 매핑 (노드 좌표 = 타일 좌표)

    예시
    ----
        g = Grid2D(20, 20)                      # 기본 4방향
        g = Grid2D(20, 20, diagonal=True)        # 8방향
        g = Grid2D(20, 20, walls={(5,5),(5,6)}) # 초기 벽
        g.add_wall((3, 4))                       # 나중에 벽 추가
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        diagonal: bool = False,
        walls: Optional[Set[Tuple[int, int]]] = None,
    ) -> None:
        self.rows     = rows
        self.cols     = cols
        self.diagonal = diagonal
        self._walls: Set[Tuple[int, int]] = set(walls) if walls else set()

    def add_wall(self, node: Tuple[int, int]) -> None:
        """노드를 벽으로 설정한다."""
        self._walls.add(node)

    def remove_wall(self, node: Tuple[int, int]) -> None:
        """벽 설정을 해제한다."""
        self._walls.discard(node)

    def is_wall(self, node: Tuple[int, int]) -> bool:
        return node in self._walls

    def wall_nodes(self) -> List[Tuple[int, int]]:
        return list(self._walls)

    @property
    def tile_rows(self) -> int:
        return self.rows

    @property
    def tile_cols(self) -> int:
        return self.cols

    def to_tile(self, node: Tuple[int, int]) -> Tuple[int, int]:
        return node

    def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """벽을 자동 제외한 유효 이웃 목록."""
        r, c = node
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.diagonal:
            dirs += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return [
            (r + dr, c + dc)
            for dr, dc in dirs
            if 0 <= r + dr < self.rows
            and 0 <= c + dc < self.cols
            and (r + dr, c + dc) not in self._walls
        ]

    def all_nodes(self) -> List[Tuple[int, int]]:
        """벽이 아닌 모든 노드 목록."""
        return [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in self._walls
        ]

    def __repr__(self) -> str:
        parts = [f"{self.rows}x{self.cols}"]
        if self.diagonal:
            parts.append("diagonal")
        if self._walls:
            parts.append(f"walls={len(self._walls)}")
        return f"Grid2D({', '.join(parts)})"


# ─────────────────────────────────────────────────────────────────────────────
# NodeGraph
# ─────────────────────────────────────────────────────────────────────────────

class NodeGraph(Structure):
    """
    임의 노드·엣지 그래프 어댑터.

    노드는 해시 가능한 값이면 무엇이든 가능.
    각 노드에 타일 (row, col) 위치를 직접 지정한다.
    TreeNode 는 이 클래스를 상속해 위치를 자동 계산한다.

    예시
    ----
        g = NodeGraph()
        g.add_node("A", tile=(0, 0))
        g.add_node("B", tile=(0, 2))
        g.add_edge("A", "B")
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed: bool                        = directed
        self._nodes:   Dict[Any, Tuple[int, int]]  = {}
        self._adj:     Dict[Any, List[Any]]        = {}

    def add_node(self, node: Any, tile: Tuple[int, int]) -> None:
        """노드를 등록한다. tile = (row, col) 타일 위치."""
        self._nodes[node] = tile
        if node not in self._adj:
            self._adj[node] = []

    def add_edge(self, u: Any, v: Any) -> None:
        """엣지를 추가한다. directed=False 이면 양방향."""
        for n in (u, v):
            if n not in self._nodes:
                raise ValueError(f"노드 {n!r} 가 등록되지 않았습니다.")
        self._adj[u].append(v)
        if not self.directed:
            self._adj[v].append(u)

    @property
    def tile_rows(self) -> int:
        return max((r for r, _ in self._nodes.values()), default=0) + 1

    @property
    def tile_cols(self) -> int:
        return max((c for _, c in self._nodes.values()), default=0) + 1

    def to_tile(self, node: Any) -> Tuple[int, int]:
        return self._nodes[node]

    def neighbors(self, node: Any) -> List[Any]:
        return list(self._adj.get(node, []))

    def all_nodes(self) -> List[Any]:
        return list(self._nodes.keys())

    def edges_as_tiles(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """엣지를 타일 좌표 쌍으로 반환. directed=False 이면 중복 제거."""
        seen: Set[Any] = set()
        result = []
        for u, adj in self._adj.items():
            for v in adj:
                key = (u, v) if self.directed else tuple(sorted([str(u), str(v)]))
                if key not in seen:
                    seen.add(key)
                    result.append((self._nodes[u], self._nodes[v]))
        return result

    def __repr__(self) -> str:
        return f"NodeGraph(nodes={len(self._nodes)}, directed={self.directed})"


# ─────────────────────────────────────────────────────────────────────────────
# TreeNode
# ─────────────────────────────────────────────────────────────────────────────

class TreeNode(NodeGraph):
    """
    트리 구조 어댑터 — 타일 위치 자동 계산.

    add(value) 로 루트를 만들고, add(value, parent=x) 로 자식을 추가한다.
    노드를 추가할 때마다 BFS 레벨 순서 기반으로 타일 위치가 자동 재계산된다.

    알고리즘 API
    ------------
        self.neighbors(node)     → 자식 목록 (directed=True)
        struct.parent_of(node)   → 부모 노드 (루트이면 None)
        struct.children_of(node) → 자식 노드 목록
        struct.root()            → 루트 노드

    레이아웃 방식
    -------------
    1. DFS(pre-order)로 리프에 순서 인덱스를 부여한다 (0, 1, 2, ...)
    2. 내부 노드의 x = 자식들 x 의 평균 (bottom-up)
    3. col = round(x * 2), row = depth * 2  (홀수 행은 엣지 통과 공간)

    이 방식은 어떤 형태의 트리에서도 겹침 없이 자연스럽게 배치된다.

    예시
    ----
        t = TreeNode()
        root = t.add(1)
        a = t.add(2, parent=1)
        b = t.add(3, parent=1)
        t.add(4, parent=2)
        t.add(5, parent=2)
        # → 자동으로 타일 위치 계산됨
    """

    def __init__(self) -> None:
        super().__init__(directed=True)   # 부모→자식 단방향
        self._parent_map:   Dict[Any, Optional[Any]] = {}
        self._children_map: Dict[Any, List[Any]]     = {}
        self._root:         Optional[Any]             = None

    # ── 트리 구성 ────────────────────────────────────────────────────

    def add(self, node: Any, parent: Optional[Any] = None) -> Any:
        """
        노드를 추가한다.

        Parameters
        ----------
        node   : 노드 식별자 (해시 가능)
        parent : 부모 노드. None 이면 루트(최초 1회만 가능).

        Returns
        -------
        node  (체이닝 편의를 위해 그대로 반환)
        """
        if parent is None:
            if self._root is not None:
                raise ValueError(
                    f"루트 '{self._root}' 가 이미 있습니다. parent 를 지정하세요."
                )
            self._root = node
        else:
            if parent not in self._children_map:
                raise ValueError(
                    f"부모 노드 '{parent}' 가 등록되지 않았습니다. "
                    "먼저 add() 로 추가하세요."
                )
            self._children_map[parent].append(node)

        self._parent_map[node]   = parent
        self._children_map[node] = []
        self._recompute_layout()
        return node

    # ── 트리 탐색 API ────────────────────────────────────────────────

    def root(self) -> Optional[Any]:
        """루트 노드를 반환한다."""
        return self._root

    def parent_of(self, node: Any) -> Optional[Any]:
        """노드의 부모를 반환한다. 루트이면 None."""
        return self._parent_map.get(node)

    def children_of(self, node: Any) -> List[Any]:
        """노드의 자식 목록을 반환한다."""
        return list(self._children_map.get(node, []))

    # ── 자동 레이아웃 ────────────────────────────────────────────────

    def _recompute_layout(self) -> None:
        """
        BFS 레벨 기반 트리 레이아웃을 재계산한다.

        알고리즘
        --------
        1. DFS pre-order 로 리프에 인덱스 0, 1, 2, ... 부여
        2. 내부 노드의 x 좌표 = 자식 x 의 평균 (반복 bottom-up BFS)
        3. col = round(x * 2),  row = depth * 2
           → 홀수 행은 아무 타일도 없어 엣지 통과 공간으로 사용됨
        """
        if self._root is None:
            return

        # ── Step 1: DFS pre-order로 리프 인덱스 부여 ─────────────────
        leaf_pos: Dict[Any, int] = {}
        leaf_counter: List[int] = [0]

        stack = [self._root]
        while stack:
            node = stack.pop()
            children = self._children_map.get(node, [])
            if not children:
                leaf_pos[node] = leaf_counter[0]
                leaf_counter[0] += 1
            else:
                for child in reversed(children):   # 왼쪽 자식 먼저 처리
                    stack.append(child)

        # ── Step 2: BFS 순서 수집 (깊이 정보 포함) ───────────────────
        bfs_order: List[Any] = []
        depth_map: Dict[Any, int] = {}
        q: deque = deque([(self._root, 0)])
        while q:
            node, depth = q.popleft()
            bfs_order.append(node)
            depth_map[node] = depth
            for child in self._children_map.get(node, []):
                q.append((child, depth + 1))

        # ── Step 3: bottom-up으로 x 좌표 계산 ────────────────────────
        x_pos: Dict[Any, float] = {}
        for node in reversed(bfs_order):
            children = self._children_map.get(node, [])
            if not children:
                x_pos[node] = float(leaf_pos[node])
            else:
                x_pos[node] = sum(x_pos[c] for c in children) / len(children)

        # ── Step 4: tile 좌표 할당 ────────────────────────────────────
        self._nodes.clear()
        self._adj.clear()

        for node in bfs_order:
            row = depth_map[node] * 2         # 짝수 행만 사용 (홀수 = 엣지 공간)
            col = int(round(x_pos[node] * 2)) # 리프 간격 2칸으로 확대
            self._nodes[node] = (row, col)
            self._adj[node]   = []

        # ── Step 5: 엣지 재구성 (parent → children) ──────────────────
        for child, parent in self._parent_map.items():
            if parent is not None:
                self._adj[parent].append(child)
                # directed=True → 역방향 엣지 추가 안 함

    def __repr__(self) -> str:
        n = len(self._nodes)
        return f"TreeNode(nodes={n}, root={self._root!r})"
