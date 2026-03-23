"""
demo_iddfs.py — 반복적 깊이 심화 탐색 (IDDFS) 시각화
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, TreeNode

class IDDFSDemo(Scene):
    def setup(self):
        # 트리를 조금 넓고 깊게 구성하여 IDDFS의 특성을 살펴봅니다.
        t = TreeNode()
        t.add("A")
        t.add("B", parent="A"); t.add("C", parent="A")
        t.add("D", parent="B"); t.add("E", parent="B")
        t.add("F", parent="C"); t.add("G", parent="C")
        t.add("H", parent="D"); t.add("I", parent="D")
        t.add("J", parent="E"); t.add("K", parent="E")
        t.add("L", parent="F"); t.add("M", parent="O") # 트리 약간 불규칙하게
        
        self.use(t)
        self.start("A")
        self.end("J") # J(깊이 3)를 목표로 설정
        
        # 알파벳 글자 출력
        for node in t.all_nodes():
            self.label(node, str(node))
            
        self.section("IDDFS (Iterative Deepening DFS)")
        self.info("핵심 개념", "제한된 깊이까지만 DFS. 실패 시 Limit 증가")
        self.info("메모리 성능", "BFS에 비해 극히 적은 메모리 사용")

    def solve(self):
        start, end = self._start_node, self._end_node
        max_depth = 4
        parent_map = {start: None}
        
        # dls 재귀 함수 내부에서 yield를 쓰려면 `yield from` 패턴이 필요합니다.
        def dls(node, target, limit, visited):
            if node == target:
                return True
            if limit <= 0:
                return False
                
            visited.add(node)
            if node != start and node != end:
                self.visit(node)
            self.info("현재 노드 (탐색 중)", node)
            yield
            
            for nb in self.neighbors(node):
                if nb not in visited:
                    parent_map[nb] = node
                    self.frontier(nb)
                    yield
                    
                    # 자식 노드로 파고듦 (재귀적 yield)
                    if (yield from dls(nb, target, limit - 1, visited)):
                        return True
                        
            # 백트래킹 (다시 돌아옴)
            visited.remove(node)
            if node != start:
                self.unvisit(node) 
            yield
            return False
            
        # 1. 메인 IDDFS 루프 (깊이를 0부터 하나씩 증가)
        for depth in range(max_depth + 1):
            self.info("현재 탐색 Limit", f"{depth} 깊이 제한!")
            
            # 매 깊이마다 트리 상태를 깨끗하게 리셋
            for n in self._struct.all_nodes():
                if n != start and n != end:
                    self.unvisit(n)
            yield
            
            visited = set()
            found = yield from dls(start, end, depth, visited)
            
            if found:
                self.info("성공!", f"깊이 {depth}에서 목표 발견!")
                # 경로(Path) 역추적 페인트
                cur = end
                while parent_map.get(cur):
                    self.path(cur)
                    cur = parent_map[cur]
                break

if __name__ == "__main__":
    IDDFSDemo().run("IDDFS 깊이 심화 탐색 시각화", config_path="vizlib.json")
