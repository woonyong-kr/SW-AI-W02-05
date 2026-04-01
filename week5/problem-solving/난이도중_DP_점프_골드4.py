# DP - 점프 (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/2253
import sys


def solution():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    m = data[1]

    stones = set()
    for i in range(2, 2 + m):
        stones.add(data[i])

    speed = int((2 * n) ** 0.5) + 2
    inf = 10**9

    dp = [[inf] * (speed + 1) for _ in range(n + 1)]
    dp[1][0] = 0

    for i in range(1, n + 1):
        if i in stones:
            continue

        for v in range(speed):
            if dp[i][v] == inf:
                continue

            for dv in (v - 1, v, v + 1):
                if dv <= 0:
                    continue

                next_stone = i + dv
                if next_stone <= n and next_stone not in stones:
                    dp[next_stone][dv] = min(dp[next_stone][dv], dp[i][v] + 1)

    result = min(dp[n])
    print(result if result != inf else -1)


if __name__ == "__main__":
    solution()
