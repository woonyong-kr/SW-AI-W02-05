# 큐 - 카드2 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/2164

import sys
from collections import deque

def solution():
    data = sys.stdin.read().split()
    if not data:
         return

    n = int(data[0])
    cards = deque([i for i in range(1, n + 1)])

    while len(cards) > 1:
            cards.popleft()
            cards.append(cards.popleft())

    print(f"{cards[0]}")

if __name__ == "__main__":
    solution()