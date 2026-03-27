# DP - 피보나치 수 2 (백준 브론즈 1)
# 문제 링크: https://www.acmicpc.net/problem/2748

import sys

def solution():
    data = sys.stdin.read()
    n = int(data)

    if n == 0:
        print(0)
        return
    if n == 1:
        print(1)
        return

    a, b = 0, 1

    for _ in range(2, n + 1):
        a, b = b, a + b

    print(b)
    
solution()