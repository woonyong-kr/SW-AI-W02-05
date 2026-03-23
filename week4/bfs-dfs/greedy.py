import heapq

def greedy_best_first(graph, start, goal, heuristic_func):
    # 방문 여부 및 경로 추적
    visited = set()
    pq = [(heuristic_func(start, goal), start)]  # (h(n), node)
    
    while pq:
        _, curr_node = heapq.heappop(pq)
        
        if curr_node == goal:
            return True # 목적지 도달
            
        if curr_node not in visited:
            visited.add(curr_node)
            for neighbor in graph[curr_node]:
                if neighbor not in visited:
                    # 미래 예측값(h)만 기준으로 큐에 삽입
                    h_n = heuristic_func(neighbor, goal)
                    heapq.heappush(pq, (h_n, neighbor))
    return False