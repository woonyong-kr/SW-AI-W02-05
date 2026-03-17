# 이분탐색 - 수 찾기 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/1920

import sys
from collections import deque

def solution():
    data = sys.stdin.read().split()
    if not data: 
         return
    
    n = int(data[0])
    base = set(data[1 : n + 1])
    targets = data[n + 2:]

    result = []
    for target in targets:
         result.append("1" if target in base else "0")

    sys.stdout.write("\n".join(result) + "\n")

if __name__ == "__main__":
    solution()