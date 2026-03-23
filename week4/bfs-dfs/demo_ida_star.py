"""
demo_ida_star.py — Iterative Deepening A* (IDA*) 시각화 
===================================================

A* 가 수만 개의 노드를 Queue 에 쌓으며 터지는 메모리 누수를 극복하기 위해,
`f_score` 제한치(Bound)를 걸고 깊이 우선(DFS) 형태로 탐색하는 혁신적인 방식입니다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, Grid2D
from vizlib.tracer import Tracer

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def ida_star(grid, start, goal, tracer):
    tracer.info("알고리즘", "IDA* (A* 최단거리 + DFS 메모리 절약)")
    
    bound = manhattan(start, goal)
    path = [start]
    
    def search(node, g, bound):
        f = g + manhattan(node, goal)
        tracer.label(node, f"F:{f}")
        
        if f > bound:
            return f, False # 현재 예산(Bound) 초과 시 백트래킹!
        if node == goal:
            return f, True
            
        tracer.visit(node)
        tracer.log_step()
        
        min_f = float('inf')
        # 4방향 탐색
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nb = (node[0]+dr, node[1]+dc)
            if 0 <= nb[0] < grid.rows and 0 <= nb[1] < grid.cols and not grid.is_wall(nb):
                if nb not in path:
                    path.append(nb)
                    tracer.frontier(nb)
                    tracer.log_step()
                    
                    t_f, found = search(nb, g + 1, bound)
                    
                    if found: return t_f, True
                    if t_f < min_f: min_f = t_f
                    
                    # DFS 라서 빠져나올때 방문 기록을 지웁니다
                    path.pop()
                    tracer.unvisit(nb)
                    tracer.log_step()
                    
        return min_f, False
        
    while True:
        tracer.info("현재 F-Bound (한계 예산)", f"{bound}점")
        tracer.log_step()
        t, found = search(start, 0, bound)
        if found:
            tracer.info("완료", "최소 비용으로 목표 도달!")
            break
        if t == float('inf'):
            break
        bound = t # 다음 반복에서 예산을 상향하여 재도전

class IDAStarDemo(Scene):
    def setup(self):
        g = Grid2D(25, 25)
        # 길목에 약간의 방해 벽 설치 (A* 였다면 큐가 수백 개 유지됨)
        for i in range(8, 18):
            g.add_wall((i, 15))
        self.use(g)
        self.start((12, 10))
        self.end((12, 18))
        self.section("IDA* (Iterative Deepening A*)")

    def solve(self):
        tracer = Tracer()
        ida_star(self._struct, self._start_node, self._end_node, tracer)
        yield from self.replay(tracer)

if __name__ == "__main__":
    IDAStarDemo().run("IDA* 시각화", config_path="vizlib.json")
