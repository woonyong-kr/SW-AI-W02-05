# 해시 테이블 - 민균이의 비밀번호 (백준 브론즈1)
# 문제 링크: https://www.acmicpc.net/problem/9933

import sys

def solution_1():
    data = sys.stdin.read().split()
    if not data: return

    n = int(data[0])
    words = data[1:]

    for i in range(n):
        mid = len(words[i]) // 2
        reversed_word = words[i][::-1]
        for j in range(i, n):
            if words[j] == reversed_word:
                print(f"{len(words[i])} {words[i][mid]}")
                return
            
def solution_2():
    data = sys.stdin.read().split()
    if not data: return

    n = int(data[0])
    words = set(data[1:])

    for word in words:
        if word[::-1] in words:
            print(f"{len(word)} {word[len(word) // 2]}")
            return

if __name__ == "__main__":
    #solution_1()
    solution_2()