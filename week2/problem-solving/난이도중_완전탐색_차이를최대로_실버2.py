# 완전탐색 - 차이를 최대로 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/10819

import sys

input_data = sys.stdin.read().split()
n = int(input_data[0])

numbers = [input_data[i] for i in range(1, input_data)]

max_value = 0
def find_max_cost(start, end, total_cost, numbers):

    if start == end:
        max_value = max(max_value, total_cost)
        return
    
    for i in range(end):


        pass

    pass