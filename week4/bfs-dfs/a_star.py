import heapq

def a_star(graph, start, goal, heuristic_func):
    # 1. g_score: 시작점에서 현재까지 온 실제 거리
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    # 2. f_score: g_score + h_score (전체 예상 비용)
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic_func(start, goal)
    
    # 우선순위 큐 (f_score, node)
    pq = [(f_score[start], start)]
    
    while pq:
        _, curr_node = heapq.heappop(pq)
        
        if curr_node == goal:
            return g_score[goal] # 최단 거리 반환
            
        for neighbor, weight in graph[curr_node].items():
            tentative_g_score = g_score[curr_node] + weight
            
            # 더 나은 경로를 찾았다면
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_n = tentative_g_score + heuristic_func(neighbor, goal)
                f_score[neighbor] = f_n
                heapq.heappush(pq, (f_n, neighbor))
                
    return float('inf')