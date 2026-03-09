# 정수론 - 소수 찾기 (백준 브론즈2)
# 문제 링크: https://www.acmicpc.net/problem/1978

import sys

input_data = sys.stdin.read().split()
t = int(input_data[0])
numbers = list(map(int, input_data[1:]))

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(n**0.5)
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
        
    return True

count = 0
for num in numbers:
   if is_prime(num):
       count += 1

print(count)