"""
demo_dfs.py — DFS (깊이 우선 탐색) 시각화
==========================================
실행:
    cd week4/bfs-dfs
    python3 demo_dfs.py

키보드:
    SPACE    : 일시정지 / 재개
    UP / DOWN: 속도 조절
    R        : 재시작
    Q        : 종료
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, Grid2D


class DFSDemo(Scene):

    def setup(self):
        g = Grid2D(25, 25)
        self.use(g)
        self.start((0, 0))
        self.end((g.rows - 1, g.cols - 1))

        self.section("DFS — 깊이 우선 탐색")
        self.section("색상 범례")
        self.info("노란색",   "frontier — 스택 대기 중")
        self.info("파란색",   "visited  — 방문 완료")
        self.info("초록색",   "start    — 출발점")
        self.info("빨간색",   "end      — 도착점")
        self.info("청록색",   "path     — 탐색된 경로")

    def solve(self):
        start, end = self._start_node, self._end_node
        stack   = [start]
        visited = set()
        parent  = {start: None}

        while stack:
            node = stack.pop()

            if node in visited:
                continue
            visited.add(node)

            if node == end:
                cur = end
                while parent[cur] is not None:
                    self.path(cur)
                    cur = parent[cur]
                return

            if node != start:
                self.visit(node)

            for nb in reversed(self.neighbors(node)):
                if nb not in visited:
                    if nb not in parent:
                        parent[nb] = node
                    self.frontier(nb)
                    stack.append(nb)

            yield


DFSDemo().run("DFS — 깊이 우선 탐색", config_path="vizlib.json")
