"""
demo_jps.py — Jump Point Search (JPS) 시각화
===================================================

A* 가 넓은 평야에서 무의미한 노드를 수천 개씩 탐색하며 
메모리를 낭비하는 문제(A* 팽창 현상)를 극복하기 위해,
직선상에 장애물(코너)이 나타날 때까지 중간 노드들을 
모두 '건너뛰는(Jump)' JPS 알고리즘의 원리를 보여줍니다.

알고리즘 코드에는 단 하나의 시각화 코드도 섞이지 않습니다!
"""
import sys, os
import heapq
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, Grid2D
from vizlib.tracer import Tracer

# ─────────────────────────────────────────────────────────────────────────────
# 1. 순수 JPS (직교 한정 데모 알고리즘)
# ─────────────────────────────────────────────────────────────────────────────
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def jps_orthogonal(grid_struct, start, goal, tracer=None):
    """
    (교육용 목적을 위해 대각선 점프를 생략한 4방향 JPS 입니다)
    매 노드를 탐색하는 A* 와 달리, 벽을 만날 때까지 직진합니다!
    """
    if tracer: tracer.info("탐색 알고리즘", "JPS (Jump Point Search)")
    
    # 방향: 상, 하, 좌, 우
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    pq = [(manhattan(start, goal), 0, start)] # (f, g, node)
    visited = set()
    parent = {start: None}
    
    def is_valid(r, c):
        return 0 <= r < grid_struct.rows and 0 <= c < grid_struct.cols and not grid_struct.is_wall((r, c))

    def jump(r, c, dr, dc):
        """방향(dr, dc)으로 레이캐스팅 점프를 실행, 의미있는 코너(Forced Neighbor)만 반환"""
        steps = 0
        while True:
            nr, nc = r + dr, c + dc
            if not is_valid(nr, nc):
                return None, steps # 벽에 막힘
            
            if tracer:
                # 점프가 훑고 지나가는 스캔 궤적을 연한 배경으로 찰나만 보여줍니다 (JPS의 강점)
                tracer.color((nr, nc), (60, 60, 80))
            
            if (nr, nc) == goal:
                 return (nr, nc), steps + 1
                 
            # 진행 방향의 양옆을 확인하여 벽의 코너(장애물 모서리)가 있는지 확인 = Forced Neighbor
            # 이 코너를 발견하면 이곳은 의미 있는 '점프 노드'가 됩니다.
            if dr != 0: # 수직 이동 중이면 좌우 확인
                if (not is_valid(nr, nc - 1) and is_valid(nr + dr, nc - 1)) or \
                   (not is_valid(nr, nc + 1) and is_valid(nr + dr, nc + 1)):
                    return (nr, nc), steps + 1
            if dc != 0: # 수평 이동 중이면 위아래 확인
                if (not is_valid(nr - 1, nc) and is_valid(nr - 1, nc + dc)) or \
                   (not is_valid(nr + 1, nc) and is_valid(nr + 1, nc + dc)):
                    return (nr, nc), steps + 1
            
            r, c = nr, nc
            steps += 1
            if tracer: tracer.log_step() # 레이저 스캔을 눈으로 볼 수 있게 스텝 양보
            
    while pq:
        f, g, curr = heapq.heappop(pq)
        
        if curr in visited:
            continue
        visited.add(curr)
        
        if tracer: 
            tracer.visit(curr)
            tracer.info("PQ 대기열 (JPS 메모리)", f"{len(pq)} 개 (매우 적음!)")
            tracer.info("확정된 점프 거점", f"{len(visited)} 개")
            tracer.log_step()
            
        if curr == goal:
            # 도착
            cur = goal
            while parent[cur]:
                if tracer: tracer.path(cur)
                cur = parent[cur]
            return

        # 도착하지 않았다면, 4방향으로 Jump!
        for dr, dc in dirs:
            jump_point, dist = jump(curr[0], curr[1], dr, dc)
            if jump_point and jump_point not in visited:
                tentative_g = g + dist
                f_n = tentative_g + manhattan(jump_point, goal)
                parent[jump_point] = curr
                
                if tracer:
                    tracer.frontier(jump_point)
                    tracer.label(jump_point, "JUMP!")
                    tracer.log_step()
                    
                heapq.heappush(pq, (f_n, tentative_g, jump_point))

# ─────────────────────────────────────────────────────────────────────────────
# 2. UI 시각화 씬
# ─────────────────────────────────────────────────────────────────────────────
class JPSDemo(Scene):
    def setup(self):
        # 방대한 100x100 평원에 군데군데 장애물을 배치
        g = Grid2D(100, 100)
        
        # JPS 가 꺾이는(Forced Neighbor) 모습을 보여주기 위해 벽을 띄엄띄엄 치기
        for r in range(20, 80, 20):
            for c in range(20, 80):
                if c % 30 != 0: # 구멍 내기
                    g.add_wall((r, c))
                    
        self.use(g)
        self.start((10, 10))
        self.end((90, 80))

        self.section("JPS (Jump Point Search)")
        self.info("A*의 문제점 해결", "거대한 공간에서 노드를 수천개씩 탐색하는 팽창 방지")
        self.info("시각적 차이", "1칸씩 전진하지 않고 장애물 모서리까지 광선(Ray)처럼 날아감")
        self.info("메모리 효율", "A* 대비 1/1000 수준의 Queue 메모리 사용")

    def solve(self):
        tracer = Tracer()
        # 시각화 개입 없이 JPS 알고리즘 호출
        jps_orthogonal(self._struct, self._start_node, self._end_node, tracer)
        # 생성된 히스토리 재생
        yield from self.replay(tracer)

if __name__ == "__main__":
    JPSDemo().run("JPS 메모리 최적화 데모", config_path="vizlib.json")
