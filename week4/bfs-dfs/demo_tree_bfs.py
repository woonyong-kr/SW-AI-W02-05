"""
demo_tree_bfs.py — 이진 트리 BFS (레벨 순서 탐색)
===================================================
실행:
    cd week4/bfs-dfs
    python3 demo_tree_bfs.py

문제 정의
---------
아래 형태의 이진 트리에서 루트(1)부터 BFS(너비 우선) 순서로 탐색한다.

             1
           /   \\
          2     3
         / \\   / \\
        4   5 6   7
       / \\
      8   9

BFS 는 같은 레벨의 노드를 먼저 처리하므로
탐색 순서: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

DFS 와의 차이
-------------
DFS 는 한 방향으로 끝까지 파고들지만 (1→2→4→8→9→5→3→6→7),
BFS 는 레벨별로 가로 방향으로 넓게 탐색한다.

키보드
------
    SPACE    : 일시정지 / 재개
    UP / DOWN: 속도 조절
    R        : 재시작
    Q        : 종료
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from collections import deque
from vizlib import Scene, TreeNode


class TreeBFSDemo(Scene):
    """이진 트리 BFS (레벨 순서 탐색) 시각화."""

    # ── 문제 정의 ──────────────────────────────────────────────────
    def setup(self):
        t = TreeNode()

        # 트리 구조 정의 (노드 값을 식별자로 사용)
        t.add(1)                     # 루트
        t.add(2, parent=1);  t.add(3, parent=1)
        t.add(4, parent=2);  t.add(5, parent=2)
        t.add(6, parent=3);  t.add(7, parent=3)
        t.add(8, parent=4);  t.add(9, parent=4)

        self.use(t)
        self.start(t.root())

        # 각 노드에 값 라벨 표시
        for node in t.all_nodes():
            self.label(node, str(node))

        self.section("Tree BFS — 레벨 순서 탐색")
        self.section("색상 범례")
        self.info("노란색",   "frontier — 큐 대기 중")
        self.info("파란색",   "visited  — 방문 완료")
        self.info("초록색",   "start    — 루트 노드")

    # ── 알고리즘 ───────────────────────────────────────────────────
    def solve(self):
        root = self._start_node
        queue   = deque([root])
        visited = {root}

        while queue:
            node = queue.popleft()

            if node != root:
                self.visit(node)

            # 자식 탐색 (TreeNode 의 neighbors = 자식 목록)
            for child in self.neighbors(node):
                if child not in visited:
                    visited.add(child)
                    self.frontier(child)
                    queue.append(child)

            yield


TreeBFSDemo().run("Tree BFS — 레벨 순서 탐색", config_path="vizlib.json")
