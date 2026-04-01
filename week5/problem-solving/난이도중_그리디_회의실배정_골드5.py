# 그리디 - 회의실 배정 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/1931
import sys


def solution():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    meetings = [(0, 0)] * n
    for i in range(1, 2 * n, 2):
        meetings[i // 2] = (data[i + 1], data[i])

    meetings = sorted(meetings)

    selected = []
    last_end = 0

    for end, start in meetings:
        if start >= last_end:
            selected.append((start, end))
            last_end = end

    print(len(selected))


if __name__ == "__main__":
    solution()
