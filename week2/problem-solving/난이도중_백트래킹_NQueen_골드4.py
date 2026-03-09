# 백트래킹 - N-Queen (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/9663

n = int(input())
board = [[0 for _ in range(n)] for _ in range(n)]

def solutions(x, n, board):

    if x == n:
        return 1
    
    count = 0
    for y in range(n):
            if board[x][y] == 0:
                update(x, y, 1)

                count += solutions(x + 1, n, board)

                update(x, y, -1)

    return count

def update(x, y, weight):
    for i in range(n):
        board[x][i] += weight
        board[i][y] += weight

    for i in range(-n, n):
        if 0 <= x + i < n and 0 <= y + i < n:
            board[x + i][y + i] += weight
        if 0 <= x + i < n and 0 <= y - i < n:
            board[x + i][y - i] += weight

print(solutions(0, n, board))