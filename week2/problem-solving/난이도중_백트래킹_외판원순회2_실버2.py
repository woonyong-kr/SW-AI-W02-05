# 백트래킹 - 외판원 순회 2 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/10971

import sys

input_data = sys.stdin.read().split()
n = int(input_data[0])

matrix = []
for i in range(n):
    start = 1 + (i * n)
    end = 1 + ((i + 1) * n)
    matrix.append(list(map(int, input_data[start:end])))    

min_value = 10**9
def find_min_cost(next_city, target, total_cost, visited):
    global min_value

    if len(visited) == target:
        return_cost = matrix[next_city][0]
        if return_cost != 0:
            min_value = min(min_value, total_cost + return_cost)
        return

    for i in range(n):
        if matrix[next_city][i] != 0 and i not in visited:
            visited.append(i)
            find_min_cost(i, target, total_cost + matrix[next_city][i], visited)
            visited.pop()

find_min_cost(0, n, 0, [0])

print(min_value)