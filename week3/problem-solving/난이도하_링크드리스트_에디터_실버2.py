# 링크드리스트 - 에디터 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/1406


import sys
from collections import deque

class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = self.next = None

def solution():
    data = sys.stdin.read().split()
    if not data: 
         return
    
    text = data[0]
    commands = data[2:]

    head, tail = Node(), Node()
    cursor = [tail]

    def link(a, b):
        a.next, b.prev = b, a

    def move(to):
        cursor[0] = to

    link(head, tail)

    ops = {
        "L": lambda: move(cursor[0].prev) if cursor[0].prev != head else None,
        "D": lambda: move(cursor[0].next) if cursor[0] != tail else None,
        "B": lambda: link(cursor[0].prev.prev, cursor[0]) if cursor[0].prev != head else None,
        "P": lambda x: (new := Node(x), link(cursor[0].prev, new), link(new, cursor[0]))
    }

    for char in text:
        ops["P"](char)

    curr = 0
    while curr < len(commands):
        cmd = commands[curr]

        if cmd == "P":
            ops["P"](commands[curr + 1])
            curr += 2
        else:
            ops[cmd]()
            curr += 1

    result, node = [], head.next
    while node != tail:
        result.append(node.data)
        node = node.next

    sys.stdout.write("".join(result) + "\n")

if __name__ == "__main__":
    solution()