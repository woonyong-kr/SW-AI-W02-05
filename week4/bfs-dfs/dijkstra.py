import heapq

def dijkstra(graph, start):
    # 1. 거리 저장소 (모든 노드 거리를 무한대로 초기화)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # 2. 우선순위 큐 (거리, 노드) - 거리가 짧은 순으로 정렬됨
    pq = [(0, start)]
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        # 이미 처리된 노드라면 스킵 (우녕님이 고민한 재할당/중복 방지)
        if curr_dist > distances[curr_node]:
            continue
            
        for neighbor, weight in graph[curr_node].items():
            distance = curr_dist + weight
            
            # 더 짧은 경로를 발견했다면 업데이트
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances