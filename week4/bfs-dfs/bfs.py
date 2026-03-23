from collections import deque

def bfs(graph, start_node):
    # 1. 방문 처리용 자료구조 (우녕님과 논의한 대로 비트마스크나 리스트로 변경 가능)
    visited = set()
    
    # 2. 큐 초기화 (시작 노드 삽입)
    queue = deque([start_node])
    visited.add(start_node)
    
    while queue:
        # 3. 큐에서 노드를 하나 꺼냄 (먼저 들어온 놈이 먼저 나감)
        curr_node = queue.popleft()
        
        # --- [로직 처리 구간] ---
        # print(f"방문: {curr_node}")
        # -----------------------
        
        # 4. 인접 노드 탐색
        for neighbor in graph[curr_node]:
            if neighbor not in visited:
                # 5. 발견 즉시 방문 처리 (큐에 중복으로 쌓이는 것을 방지)
                visited.add(neighbor)
                queue.append(neighbor)