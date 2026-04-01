# 그리디 - 신입 사원 (백준 실버1)
# 문제 링크: https://www.acmicpc.net/problem/1946
import sys


def solution():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]

    i = 1
    for _ in range(t):
        n = data[i]
        i += 1

        result = []
        for _ in range(n):
            grade1 = data[i]
            grade2 = data[i + 1]
            i += 2
            result.append((grade1, grade2))

        result.sort()

        count = 1
        best = result[0][1]

        for i in range(1, n):
            if result[i][1] < best:
                count += 1
                best = result[i][1]

        print(count)


if __name__ == "__main__":
    solution()
