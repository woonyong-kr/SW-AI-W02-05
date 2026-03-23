"""
demo_bfs_dfs_graph.py — BFS 와 DFS 의 심도깊은 차이 (네트워크/그래프 위 탐색)
===================================================

단순 격자 기반의 단방향 전진으로는 DFS와 BFS의 차이가 미미해보이기 때문에,
노드-링크 네트워크 형태로 두 탐색의 성향을 극명하게 대비시키는 데모입니다.
"""
import sys, os
from collections import deque
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, NodeGraph
from vizlib.tracer import Tracer

# ─────────────────────────────────────────────────────────────────────────────
# 1. 시각화가 분리된 순수 알고리즘
# ─────────────────────────────────────────────────────────────────────────────
def run_bfs(graph, start, goal, tracer):
    q = deque([start])
    visited = {start}
    tracer.info("알고리즘", "BFS (너비 우선)")
    tracer.info("탐색 성향", "모든 방향을 1칸씩 동시에 훑음 (물결 파장)")
    
    while q:
        curr = q.popleft()
        tracer.visit(curr)
        tracer.log_step()
        if curr == goal: return
        for nb in graph.neighbors(curr):
            if nb not in visited:
                visited.add(nb)
                tracer.frontier(nb)
                q.append(nb)
        tracer.log_step()

def run_dfs(graph, start, goal, tracer):
    stack = [start]
    visited = set()
    parent = {start: None}
    tracer.info("알고리즘", "DFS (깊이 우선)")
    tracer.info("탐색 성향", "한 루트를 끝까지 파고 듦 (맹목적 직진)")
    
    while stack:
        curr = stack.pop()
        if curr in visited: continue
        visited.add(curr)
        tracer.visit(curr)
        tracer.log_step()
        if curr == goal: return
        for nb in reversed(graph.neighbors(curr)):
            if nb not in visited:
                tracer.frontier(nb)
                if nb not in parent:
                    parent[nb] = curr
                stack.append(nb)
        tracer.log_step()

# ─────────────────────────────────────────────────────────────────────────────
# 2. UI 시각화 씬
# ─────────────────────────────────────────────────────────────────────────────
class BFSDFSDemo(Scene):
    def setup(self):
        g = NodeGraph(directed=False)
        center = "Core"
        cx, cy = 50, 50 # 거대 가상 좌표 중심 중앙
        g.add_node(center, tile=(cx, cy))
        
        # 기하학적인 초거대 거미줄(Spiderweb) 그래프를 생성해 예술적인 시각화 연출!!
        import math
        rings = 4 # 깊이 4단계 거미줄 (가운데 포함 총 5단계)
        nodes_per_ring = [8, 16, 24, 32] # 바깥쪽으로 갈수록 노드가 많아짐
        
        prev_ring = [center]
        node_id = 1
        
        for r, num_nodes in enumerate(nodes_per_ring):
            radius = (r + 1) * 11
            current_ring = []
            
            for i in range(num_nodes):
                angle = (i / num_nodes) * 2 * math.pi
                tr = cx + int(math.sin(angle) * radius)
                tc = cy + int(math.cos(angle) * radius)
                name = f"N{node_id}" 
                g.add_node(name, tile=(tr, tc))
                current_ring.append(name)
                
                # 거미줄 세로 연결 (상위 부모에 매핑)
                parent_idx = int((i / num_nodes) * len(prev_ring))
                g.add_edge(prev_ring[parent_idx], name)
                
                # 거미줄 가로 연결 (가로 망)
                if i > 0:
                    g.add_edge(name, current_ring[-2])
                node_id += 1
            
            # 마지막 노드와 첫 노드 가로 연결
            g.add_edge(current_ring[-1], current_ring[0])
            prev_ring = current_ring

        self.use(g)
            
        self.start("Core")
        self.end(prev_ring[15]) # 가장 바깥쪽의 임의의 노드를 목적지로
        self.section("파장 vs 수직 파고들기")
        self.info("BFS", "거미줄의 가장 안쪽부터 한 껍질씩 뻗어나갑니다")
        self.info("DFS", "거미줄의 가장 바깥 껍질까지 무식하게 직진합니다")

    def solve(self):
        tracer = Tracer()
        
        # 1. BFS 시연
        run_bfs(self._struct, self._start_node, self._end_node, tracer)
        yield from self.replay(tracer)
        
        # (리셋)
        tracer.events.clear()
        for n in self._struct.all_nodes():
            tracer.unvisit(n)
        tracer.start(self._start_node)
        tracer.end(self._end_node)
        tracer.log_step()
        
        # 2. DFS 시연
        run_dfs(self._struct, self._start_node, self._end_node, tracer)
        yield from self.replay(tracer)

if __name__ == "__main__":
    BFSDFSDemo().run("BFS vs DFS 극명한 비교", config_path="vizlib.json")
