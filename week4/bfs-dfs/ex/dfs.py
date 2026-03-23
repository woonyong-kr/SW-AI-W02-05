def dfs_recursive(graph, node, visited):
    # 방문했던 노드가 아니라면 등록 / 시작 노드
    visited.add(node)
    
    # --- [로직 처리 구간] ---
    
    # -----------------------
    
    # 인접 노드 깊게 탐색
    for neighbor in graph[node]:
        if neighbor not in visited:
            # 재귀 호출 (시스템 스택 사용)
            dfs_recursive(graph, neighbor, visited)


def dfs_iterative(graph, start_node):
    visited = set()
    # 스택 초기화
    stack = [start_node]
    
    while stack:
        # 가장 나중에 들어온 놈을 꺼냄
        curr_node = stack.pop()
        
        if curr_node not in visited:
            # 방문 처리
            visited.add(curr_node)
            
            # --- [로직 처리 구간] ---

            # -----------------------
            
            # 인접 노드 스택에 삽입 (역순으로 넣으면 재귀와 순서가 같아짐)
            for neighbor in reversed(graph[curr_node]):
                if neighbor not in visited:
                    stack.append(neighbor)