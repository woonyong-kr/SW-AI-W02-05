# DP - 동전 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/9084
import sys


def solution():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    i = 1
    answers = []

    for _ in range(t):
        n = data[i]
        i += 1

        coins = data[i : i + n]
        i += n

        m = data[i]
        i += 1

        dp = [0] * (m + 1)
        dp[0] = 1

        for coin in coins:
            for money in range(coin, m + 1):
                dp[money] += dp[money - coin]

        answers.append(str(dp[m]))

    print("\n".join(answers))


if __name__ == "__main__":
    solution()
