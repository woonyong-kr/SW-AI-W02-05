# 문자열 - 문자열 반복 (백준 브론즈2)
# 문제 링크: https://www.acmicpc.net/problem/2675

import sys

data = iter(sys.stdin.read().split())

c = int(next(data))

result = ["" for _ in range(c)]
for i in range(c):
    r = int(next(data))
    s = next(data)
    result[i] = "".join(result[i] + char * r for char in s)

for res in result:
    print(res)
