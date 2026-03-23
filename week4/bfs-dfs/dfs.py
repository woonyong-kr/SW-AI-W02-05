def dfs_recursive(graph, node, visited):
    # 1. 현재 노드 방문 처리
    visited.add(node)
    
    # --- [로직 처리 구간] ---
    # print(f"방문: {node}")
    # -----------------------
    
    # 2. 인접 노드 깊게 탐색
    for neighbor in graph[node]:
        if neighbor not in visited:
            # 3. 재귀 호출 (시스템 스택 사용)
            dfs_recursive(graph, neighbor, visited)

# 사용 시:
# visited_set = set()
# dfs_recursive(graph, start, visited_set)

def dfs_iterative(graph, start_node):
    visited = set()
    # 1. 스택 초기화
    stack = [start_node]
    
    while stack:
        # 2. 가장 나중에 들어온 놈을 꺼냄
        curr_node = stack.pop()
        
        if curr_node not in visited:
            # 3. 방문 처리
            visited.add(curr_node)
            
            # --- [로직 처리 구간] ---
            # -----------------------
            
            # 4. 인접 노드 스택에 삽입 (역순으로 넣으면 재귀와 순서가 같아짐)
            for neighbor in reversed(graph[curr_node]):
                if neighbor not in visited:
                    stack.append(neighbor)