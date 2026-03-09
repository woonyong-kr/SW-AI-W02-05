# 파이썬 문법 - 최댓값 (백준 브론즈3)
# 문제 링크: https://www.acmicpc.net/problem/2562

numbers = []
for _ in range(9):
    numbers.append(int(input()))
    
max_number = max(numbers)
max_number_index = numbers.index(max_number) + 1

print(max_number)
print(max_number_index)