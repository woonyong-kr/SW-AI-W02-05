import heapq

def dijkstra(graph, start):
    # 조건 / 모든 노드 거리를 무한대로 초기화
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # 거리가 짧은 순으로 정렬
    pq = [(0, start)]
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        # 조건 / 이미 처리된 노드라면 스킵 / 갈수 없는 길이라면 스킵
        if curr_dist > distances[curr_node]:
            continue
    
        for neighbor, weight in graph[curr_node].items():
            distance = curr_dist + weight
            
            # 더 짧은 경로를 발견했다면 업데이트
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances