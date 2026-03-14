class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self._size = 0
        if iterable:
            for item in iterable:
                self.append(item)

    def append(self, x):
        new_node = Node(x)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def insert(self, i, x):
        if i < 0:
            i = max(0, self._size + i)
        i = min(i, self._size)
        new_node = Node(x)
        if self._size == 0:
            self.head = new_node
            self.tail = new_node
        elif i == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        elif i == self._size:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        else:
            cur = self._node_at(i)
            new_node.next = cur
            new_node.prev = cur.prev
            cur.prev.next = new_node
            cur.prev = new_node
        self._size += 1

    def remove(self, x):
        cur = self.head
        while cur:
            if cur.data == x:
                self._unlink(cur)
                return
            cur = cur.next
        raise ValueError(f"{x}은(는) 리스트에 없습니다")

    def pop(self, i=-1):
        if self._size == 0:
            raise IndexError("빈 리스트에서 pop할 수 없습니다")
        if i < 0:
            i = self._size + i
        if i < 0 or i >= self._size:
            raise IndexError("pop 인덱스가 범위를 벗어났습니다")
        node = self._node_at(i)
        val = node.data
        self._unlink(node)
        return val

    def index(self, x, start=0, stop=None):
        if stop is None:
            stop = self._size
        cur = self.head
        for i in range(self._size):
            if i >= stop:
                break
            if i >= start and cur.data == x:
                return i
            cur = cur.next
        raise ValueError(f"{x}은(는) 리스트에 없습니다")

    def count(self, x):
        cnt = 0
        cur = self.head
        while cur:
            if cur.data == x:
                cnt += 1
            cur = cur.next
        return cnt

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def clear(self):
        self.head = None
        self.tail = None
        self._size = 0

    def _node_at(self, i):
        if i < self._size // 2:
            cur = self.head
            for _ in range(i):
                cur = cur.next
        else:
            cur = self.tail
            for _ in range(self._size - 1 - i):
                cur = cur.prev
        return cur

    def _unlink(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self._size -= 1

    def __len__(self):
        return self._size

    def __getitem__(self, i):
        if i < 0:
            i = self._size + i
        if i < 0 or i >= self._size:
            raise IndexError("리스트 인덱스가 범위를 벗어났습니다")
        return self._node_at(i).data

    def __setitem__(self, i, x):
        if i < 0:
            i = self._size + i
        if i < 0 or i >= self._size:
            raise IndexError("리스트 할당 인덱스가 범위를 벗어났습니다")
        self._node_at(i).data = x

    def __delitem__(self, i):
        self.pop(i)

    def __contains__(self, x):
        cur = self.head
        while cur:
            if cur.data == x:
                return True
            cur = cur.next
        return False

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next

    def __repr__(self):
        return "[" + ", ".join(repr(x) for x in self) + "]"


if __name__ == "__main__":
    dll = DoublyLinkedList([1, 2, 3])
    dll.insert(0, 0)
    print(dll)           # [0, 1, 2, 3]

    dll.remove(2)
    print(dll)           # [0, 1, 3]

    print(dll.pop())     # 3
    print(dll.pop(0))    # 0
    print(dll)           # [1]

    dll.extend([2, 3])
    print(dll)           # [1, 2, 3]
    print(dll[1])        # 2
    print(2 in dll)      # True
    print(dll.index(3))  # 2
    print(dll.count(2))  # 1
    print(len(dll))      # 3

    dll[0] = 9
    print(dll)           # [9, 2, 3]

    del dll[1]
    print(dll)           # [9, 3]

    dll.clear()
    print(dll)           # []
