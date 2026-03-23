from collections import deque

def bfs(graph, start_node):
    # 방문했던 노드가 아니라면 등록
    visited = set()
    
    # 시작 등록
    queue = deque([start_node])
    visited.add(start_node)
    
    while queue:
        # 탐색 대상
        curr_node = queue.popleft()
        
        # --- [로직 처리 구간] ---
        
        # -----------------------
        
        # 인접 노드 탐색
        for neighbor in graph[curr_node]:
            if neighbor not in visited:
                # 발견 즉시 방문 처리 (큐에 중복으로 쌓이는 것을 방지)
                visited.add(neighbor)
                queue.append(neighbor)