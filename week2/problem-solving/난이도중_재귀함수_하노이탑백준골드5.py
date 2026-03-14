# 재귀함수 - 하노이 탑 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/1914

n = int(input())

def hanoi(n, start, end, sub):
    if n == 1:
        print(f"{start} {end}")
        return
    
    hanoi(n - 1, start, sub, end)
    print(f"{start} {end}")
    hanoi(n - 1, sub, end, start)


print(2**n - 1)

if n <= 20:
    hanoi(n, 1, 3, 2)

    #4 1 3 2
        #3 1 2 3
            #2 1 3 2
                #1 1 3 2
    #1 3 2
    #1 3 2
    #1 3 2
