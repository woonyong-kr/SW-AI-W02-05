"""
demo_topological_sort.py — 위상 정렬 (Topological Sort)
===================================================

순수 알고리즘(`topological_sort`)과 시각화(`TopoDemo`)가 
어떻게 완벽하게 분리되어 동작하는지 보여주는 데모입니다.
"""
import sys, os
from collections import deque
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, NodeGraph
from vizlib.tracer import Tracer

# ─────────────────────────────────────────────────────────────────────────────
# 1. 시각화 코드가 전혀 없는 "순수 알고리즘 (위상 정렬)"
# ─────────────────────────────────────────────────────────────────────────────
def topological_sort(graph_nodes, get_neighbors, tracer=None):
    """
    Kahn's Algorithm (진입 차수 기반 위상 정렬)
    
    graph_nodes  : 전체 노드 리스트
    get_neighbors: 특정 노드의 이웃(도착점)을 반환하는 함수
    tracer       : 시각화를 위한 옵저버 객체 (선택)
    """
    # 1. 진입 차수(in-degree) 계산
    in_degree = {n: 0 for n in graph_nodes}
    for u in graph_nodes:
        for v in get_neighbors(u):
            in_degree[v] += 1
            
    if tracer:
        for n, deg in in_degree.items():
            tracer.label(n, f"In:{deg}")
    if tracer: tracer.log_step()

    # 2. 진입 차수가 0인 노드를 큐에 삽입
    queue = deque([n for n in graph_nodes if in_degree[n] == 0])
    
    if tracer:
        for n in queue:
            tracer.frontier(n)
            tracer.color(n, (200, 150, 0)) # 대기 큐 강조
    if tracer: tracer.log_step()

    result = []
    
    # 3. 큐에서 꺼내며 위상 정렬 수행
    while queue:
        u = queue.popleft()
        result.append(u)
        
        if tracer:
            tracer.visit(u)
            tracer.info("위상 정렬 결과", " → ".join(result))
            tracer.log_step()
            
        for v in get_neighbors(u):
            in_degree[v] -= 1
            
            if tracer:
                tracer.label(v, f"In:{in_degree[v]}")
                tracer.color(v, (150, 50, 150)) # 갱신됨
                tracer.log_step()
                
            if in_degree[v] == 0:
                queue.append(v)
                if tracer:
                    tracer.frontier(v)
                    tracer.color(v, (200, 150, 0))
                if tracer: tracer.log_step()
                
    return result

# ─────────────────────────────────────────────────────────────────────────────
# 2. 시각화 (UI) 엔진
# ─────────────────────────────────────────────────────────────────────────────
class TopoDemo(Scene):
    def setup(self):
        # 밋밋한 수동 코딩 대신, 30개 이상의 노드가 얽힌 거대한 MMORPG 스킬 트리를
        # 알고리즘으로 자동 생성(Procedural Generation) 하여 시각적 압도감을 줍니다!
        g = NodeGraph(directed=True)
        import random
        random.seed(42) # 동일한 그래프 유지를 위한 시드 고정
        
        layers = 6
        nodes_by_layer = []
        node_id = 1
        
        for layer in range(layers):
            layer_nodes = []
            num_nodes = random.randint(4, 7) # 각 층마다 4~7 개의 스킬 노드
            row = 5 + layer * 15 # 층이 내려갈수록 아래로
            col_spacing = 80 // num_nodes
            
            for i in range(num_nodes):
                col = 15 + i * col_spacing + random.randint(-3, 3)
                name = f"S{node_id}"
                g.add_node(name, tile=(row, col))
                layer_nodes.append(name)
                
                # 이전 계층의 상위 스킬(부모)들을 1~3개 화살표 선행 무작위 연결
                if layer > 0:
                    parents = random.sample(nodes_by_layer[-1], k=random.randint(1, min(3, len(nodes_by_layer[-1]))))
                    for p in parents:
                        g.add_edge(p, name)
                node_id += 1
            nodes_by_layer.append(layer_nodes)
        
        self.use(g)
        
        for n in g.all_nodes():
            self.label(n, "") # 이름 대신 in-degree가 들어갈 것!
            
        self.section("거대 스킬 트리 위상 정렬")
        self.info("설명", "30개 규모의 거대한 절차지향 트리도 완벽히 소화합니다")
        self.info("특징", "옵저버(Tracer) 분리 및 네온사인 테마 적용 완벽 지원!")

    def solve(self):
        tracer = Tracer()
        # 시각화 개입 없이 순수 알고리즘만 호출!
        topological_sort(
            self._struct.all_nodes(),
            self.neighbors,
            tracer
        )
        
        # 알고리즘이 끝난 후, 기록된 히스토리를 애니메이션 방영
        yield from self.replay(tracer)

if __name__ == "__main__":
    TopoDemo().run("위상정렬(DAG) 독립 구조 데모", config_path="vizlib.json")
