# 정수론 - 골드바흐의 추측 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/9020

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

result = []
for num in numbers:

    a = num // 2
    b = num // 2
    
    while a >= 2:
        if is_prime(a) and is_prime(b):
            result.append((a, b))
            break
        else:
            a -= 1
            b += 1

for res in result:
    print(f"{res[0]} {res[1]}")

            

