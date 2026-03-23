"""
demo_dijkstra.py — 다익스트라(Dijkstra) 알고리즘 시각화
"""
import sys, os
import heapq
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, Grid2D

class DijkstraDemo(Scene):
    def setup(self):
        g = Grid2D(25, 25)
        self.swamp = set()
        
        # 다익스트라의 진가를 보여주는 '가중치' 개념 (늪지대)
        # 장애물이 아니지만 통과 비용이 5인 늪지대를 넓게 배치합니다.
        for r in range(5, 15):
            for c in range(10, 15):
                self.swamp.add((r, c))
                
        # 약간의 완전 벽
        for i in range(10, 20):
            g.add_wall((i, 20))
            
        self.use(g)
        self.start((0, 0))
        self.end((g.rows - 1, g.cols - 1))

        self.section("다익스트라 (Dijkstra) 탐색")
        self.section("색상 범례")
        self.info("녹색(숫자5)", "Swamp (늪지대) — 통과 비용 5")
        self.info("노드 숫자", "출발점으로부터의 현재까지 누적 최단 거리")
        self.info("파란색",   "visited  — 탐색 확정")

    def solve(self):
        # 늪지대 색칠하기 (시각화 효과)
        for s in self.swamp:
            self.color(s, (50, 150, 50))
            self.label(s, "5")
        yield

        start, end = self._start_node, self._end_node
        
        # 1. 거리 저장소
        distances = {start: 0}
        parent = {start: None}
        
        # 2. 우선순위 큐 (거리, (r, c))
        pq = [(0, start)]
        visited = set()
        
        while pq:
            curr_dist, curr_node = heapq.heappop(pq)
            
            # 큐에 중복으로 들어갔던 더 긴 경로는 무시
            if curr_node in visited:
                continue
                
            visited.add(curr_node)
            
            # 목표 지점 도달 시 역추적
            if curr_node == end:
                cur = end
                while parent[cur] is not None:
                    self.path(cur)
                    cur = parent[cur]
                self.info("완료!", "늪을 피해 더 먼 길로 최단 비용 경로를 찾음")
                return
                
            if curr_node != start:
                self.visit(curr_node)
                
            # 이웃 탐색 (Grid2D의 상하좌우 탐색)
            for nb in self.neighbors(curr_node):
                if nb in visited:
                    continue
                    
                # 핵심: 늪지대인 경우 비용이 5
                weight = 5 if nb in self.swamp else 1
                distance = curr_dist + weight
                
                # 기존에 알려진 거리보다 짧으면 업데이트
                if distance < distances.get(nb, float('inf')):
                    distances[nb] = distance
                    parent[nb] = curr_node
                    
                    self.label(nb, str(distance)) # 현재 갱신된 거리 표시
                    self.frontier(nb)
                    heapq.heappush(pq, (distance, nb))
                    
            self.info("우선순위 큐 (PQ) 크기", len(pq))
            yield

if __name__ == "__main__":
    DijkstraDemo().run("다익스트라(Dijkstra) 시각화", config_path="vizlib.json")
