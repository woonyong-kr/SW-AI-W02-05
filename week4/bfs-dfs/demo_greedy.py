"""
demo_greedy.py — 그리디 베스트우선 탐색 (Greedy Best-First) 시각화
"""
import sys, os
import heapq
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, Grid2D

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class GreedyDemo(Scene):
    def setup(self):
        g = Grid2D(25, 25)
        # 장애물을 'ㄷ'자 함정 형태로 배치 (도착지 바로 앞)
        for i in range(5, 18):
            g.add_wall((i, 18))
        for i in range(15, 21):
            g.add_wall((5, i))
            g.add_wall((17, i))
            
        self.use(g)
        self.start((11, 8))
        self.end((11, 23)) # ㄷ자 함정 안에 도착지 배치

        self.section("Greedy BFS 탐색")
        self.info("특징", "거대한 벽 함정에 무지성으로 빠지는 약점 전시!")
        self.info("노드 글자", "도착지까지의 예측 H(휴리스틱) 점수 표시")

    def solve(self):
        start, end = self._start_node, self._end_node
        
        # 실제 비용을 무시하고 남은 거리(h)만으로 진행
        pq = [(manhattan(start, end), start)]
        visited = set()
        parent = {start: None}
        
        while pq:
            _, curr_node = heapq.heappop(pq)
            
            if curr_node in visited:
                continue
                
            visited.add(curr_node)
            
            if curr_node == end:
                cur = end
                while parent[cur] is not None:
                    self.path(cur)
                    cur = parent[cur]
                self.info("완료!", "도착했지만, 최단경로가 아닐 수 있습니다.")
                return
                
            if curr_node != start:
                self.visit(curr_node)
                
            for nb in self.neighbors(curr_node):
                if nb not in visited:
                    h_n = manhattan(nb, end)
                    parent[nb] = curr_node
                    self.label(nb, f"H{h_n}") # 예측된 휴리스틱만 시각적으로 표시
                    self.frontier(nb)
                    heapq.heappush(pq, (h_n, nb))
                    
            self.info("우선순위 큐 (PQ) 크기", len(pq))
            yield

if __name__ == "__main__":
    GreedyDemo().run("Greedy BFS 시각화", config_path="vizlib.json")
