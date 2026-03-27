# DP - 01타일 (백준 실버3)
# 문제 링크: https://www.acmicpc.net/problem/1904

import sys

def solution():
    data = sys.stdin.read()
    n = int(data)

    if n == 1:
        print(1)
        return
    if n == 2:
        print(2)
        return

    a, b = 1, 2

    for _ in range(3, n + 1):
        a, b = b, (a + b) % 15746

    print(b)
    
solution()