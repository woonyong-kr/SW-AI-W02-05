# 그리디 - 동전 0 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/11047


import sys

def solution():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    coins = list(map(int, data[2:]))

    total = 0
    for coin in reversed(coins):
        if k <= 0:
            break

        total += k // coin
        k %= coin

    print(total)

solution()