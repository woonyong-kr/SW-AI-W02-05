# 그리디 - 잃어버린 괄호 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/1541

import sys

def solution():
    data = sys.stdin.read().split("-")

    result = 0
    for i in range(len(data)):
        group_sum = sum(int(a) for a in data[i].split("+"))

        if i == 0:
            result += group_sum
        else:
            result -= group_sum
    
    print(result)
    
solution()