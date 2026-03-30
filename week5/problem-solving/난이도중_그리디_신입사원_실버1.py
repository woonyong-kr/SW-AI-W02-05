# 그리디 - 신입 사원 (백준 실버1)
# 문제 링크: https://www.acmicpc.net/problem/1946

import sys

def solution():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1

    cases = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        applicants = []
        for _ in range(n):
            doc = data[idx]
            interview = data[idx + 1]
            applicants.append((doc, interview))
            idx += 2

        cases.append(applicants)
        
    result = 0
    
    print(result)
    
solution()