"""
demo_hpa_concept.py — HPA* 알고리즘 공간 추상화 (계층화) 시각화
===================================================

수백만 타일을 매 픽셀마다 세며 계산하면 A* 도 마비됩니다.
10x10 사이즈의 거대한 '구역(Room)'으로 맵을 쪼개고, 
서로 넘어갈 수 있는 '문(Door/Gateway)'만 노드로 등록하여 그래프를 축소시킵니다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, NodeGraph
from vizlib.tracer import Tracer

class HPADemo(Scene):
    def setup(self):
        # 전체 맵을 '문(Gateway)' 노드 로만 구성한 매크로(Macro) 그래프입니다.
        g = NodeGraph(directed=False)
        
        # 4개의 큰 방이 있다고 가정하고 그 경계의 문들
        g.add_node("Door (A-B)", tile=(8, 12))  # A방에서 B방 가는 문
        g.add_node("Door (B-C)", tile=(12, 16)) # B방에서 C방 가는 문
        g.add_node("Door (C-D)", tile=(16, 12)) # C방에서 D방 가는 문
        g.add_node("Door (D-A)", tile=(12, 8))  # D방에서 A방 가는 문
        
        # 각 문 사이에 방을 가로지르는 '매크로 간선' (이미 A*로 거리가 계산된 상태)
        g.add_edge("Door (A-B)", "Door (B-C)")
        g.add_edge("Door (B-C)", "Door (C-D)")
        g.add_edge("Door (C-D)", "Door (D-A)")
        g.add_edge("Door (D-A)", "Door (A-B)")
        
        self.use(g)
        for n in g.all_nodes():
            self.label(n, n)
            
        self.start("Door (D-A)")
        self.end("Door (B-C)")
        
        self.section("HPA* (계층적 길찾기)")
        self.info("핵심 철학", "타일을 잊어라! 전체 맵을 방과 문의 개념으로 묶어라.")
        self.info("퍼포먼스", "먼 목적지를 찾을 때 노드 탐색 수가 수백 배 감소")

    def solve(self):
        tracer = Tracer()
        
        tracer.info("HPA* 1단계", "개별 타일이 아닌 거대한 문(Door) 위주로 Macro 탐색")
        tracer.log_step()
        
        # Macro BFS 
        tracer.visit("Door (D-A)")
        tracer.log_step()
        
        tracer.frontier("Door (A-B)")
        tracer.frontier("Door (C-D)")
        tracer.log_step()
        
        tracer.visit("Door (A-B)")
        tracer.log_step()
        
        tracer.frontier("Door (B-C)")
        tracer.log_step()
        
        tracer.visit("Door (B-C)")
        tracer.log_step()
        
        tracer.info("HPA* 2단계", "거점(Door) 간 거시적 경로 확정 (빨간 선)")
        tracer.path("Door (D-A)")
        tracer.path("Door (A-B)")
        tracer.path("Door (B-C)")
        tracer.log_step()
        
        tracer.info("HPA* 3단계", "실제로 캐릭터가 이동할 때, 두 문 사이의 방(Room) 안에서만 미시적 A* 실행!")
        yield from self.replay(tracer)

if __name__ == "__main__":
    HPADemo().run("HPA* 공간 추상화 개념", config_path="vizlib.json")
