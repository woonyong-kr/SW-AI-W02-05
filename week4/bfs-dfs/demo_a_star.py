"""
demo_a_star.py — A* 알고리즘 시각화
"""
import sys, os
import heapq
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, Grid2D

def manhattan(a, b):
    # x 차이 + y 차이 (휴리스틱 함수)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class AStarDemo(Scene):
    def setup(self):
        g = Grid2D(25, 25)
        # 그리디와 똑같은 거대한 함정을 설치해, F=G+H 원리가 
        # 어떻게 함정에서 지능적으로 탈출하는지 비교합니다.
        for i in range(5, 18):
            g.add_wall((i, 18))
        for i in range(15, 21):
            g.add_wall((5, i))
            g.add_wall((17, i))
            
        self.use(g)
        self.start((11, 8))
        self.end((11, 23))

        self.section("A* (A-Star) 탐색")
        self.info("특징", "Greedy처럼 함정에 끌리지만, G비용 증가로 우회함")
        self.info("노드 숫자", "최종 예측 비용인 F점수 표시 (F=G+H)")

    def solve(self):
        start, end = self._start_node, self._end_node
        
        g_score = {start: 0}
        f_score = {start: manhattan(start, end)}
        parent = {start: None}
        
        # (f_score, 노드좌표)
        pq = [(f_score[start], start)]
        visited = set()
        
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
                self.info("완료!", "탐색 노드가 훨씬 적은 것을 확인하세요.")
                return
                
            if curr_node != start:
                self.visit(curr_node)
                
            for nb in self.neighbors(curr_node):
                if nb in visited:
                    continue
                    
                tentative_g = g_score.get(curr_node, float('inf')) + 1
                
                if tentative_g < g_score.get(nb, float('inf')):
                    g_score[nb] = tentative_g
                    f_n = tentative_g + manhattan(nb, end)
                    f_score[nb] = f_n
                    parent[nb] = curr_node
                    
                    self.label(nb, str(f_n)) # A*의 두뇌 해킹: 노드에 F스코어 작성
                    self.frontier(nb)
                    heapq.heappush(pq, (f_n, nb))
                    
            self.info("우선순위 큐 (PQ) 크기", len(pq))
            yield

if __name__ == "__main__":
    AStarDemo().run("A* 시각화", config_path="vizlib.json")
