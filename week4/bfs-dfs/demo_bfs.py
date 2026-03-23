"""
demo_bfs.py — BFS (너비 우선 탐색) 시각화
==========================================
실행:
    cd week4/bfs-dfs
    python3 demo_bfs.py

키보드:
    SPACE    : 일시정지 / 재개
    UP / DOWN: 속도 조절
    R        : 재시작
    Q        : 종료
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from collections import deque
from vizlib import Scene, Grid2D


class BFSDemo(Scene):

    def setup(self):
        g = Grid2D(25, 25)
        self.use(g)
        self.start((0, 0))
        self.end((g.rows - 1, g.cols - 1))

        self.section("BFS — 너비 우선 탐색")
        self.section("색상 범례")
        self.info("노란색",   "frontier — 큐 대기 중")
        self.info("파란색",   "visited  — 방문 완료")
        self.info("초록색",   "start    — 출발점")
        self.info("빨간색",   "end      — 도착점")
        self.info("청록색",   "path     — 최단 경로")

    def solve(self):
        start, end = self._start_node, self._end_node
        queue   = deque([start])
        visited = {start}
        parent  = {start: None}

        while queue:
            node = queue.popleft()

            if node == end:
                cur = end
                while parent[cur] is not None:
                    self.path(cur)
                    cur = parent[cur]
                return

            if node != start:
                self.visit(node)

            for nb in self.neighbors(node):
                if nb not in visited:
                    visited.add(nb)
                    parent[nb] = node
                    self.frontier(nb)
                    queue.append(nb)

            yield


BFSDemo().run("BFS — 너비 우선 탐색", config_path="vizlib.json")
