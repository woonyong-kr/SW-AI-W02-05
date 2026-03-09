# 배열 - 평균은 넘겠지 (백준 브론즈1)
# 문제 링크: https://www.acmicpc.net/problem/4344

import sys

data = iter(map(int, sys.stdin.read().split()))

c = next(data)

for _ in range(c):
    n = next(data)
    scores = []
    for _ in range(n):
        scores.append(next(data))

    average = sum(scores) / n
    above_average_student_count = 0
    for score in scores:
        if score > average:
            above_average_student_count += 1
    print(f"{(above_average_student_count / n) * 100:.3f}%")