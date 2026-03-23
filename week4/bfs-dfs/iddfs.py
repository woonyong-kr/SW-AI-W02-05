def depth_limited_search(graph, node, target, limit, visited):
    """
    특정 깊이(limit)까지만 파고드는 DFS
    """
    if node == target:
        return True
    if limit <= 0:
        return False
    
    visited.add(node)
    
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            # 깊이를 1 줄여서 재귀 호출 (남은 거리가 limit)
            if depth_limited_search(graph, neighbor, target, limit - 1, visited):
                return True
                
    # 백트래킹: 다른 경로에서 이 노드를 다시 방문할 수 있도록 제거
    visited.remove(node)
    return False

def iddfs(graph, start, target, max_depth):
    """
    IDDFS 메인 루프: 깊이를 0부터 하나씩 늘려가며 DLS 호출
    """
    for depth in range(max_depth + 1):
        # 매 깊이마다 방문 리스트를 새로 초기화 (새로운 탐색 시작)
        visited = set()
        if depth_limited_search(graph, start, target, depth, visited):
            print(f"목표 발견! 깊이: {depth}")
            return True
    return False