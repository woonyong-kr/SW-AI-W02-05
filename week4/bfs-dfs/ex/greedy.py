import heapq

import math

def heuristic_func(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def greedy_best_first(graph, start, goal, heuristic_func):
    # 방문했던 노드가 아니라면 등록
    visited = set()

    pq = [(heuristic_func(start, goal), start)] 
    
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