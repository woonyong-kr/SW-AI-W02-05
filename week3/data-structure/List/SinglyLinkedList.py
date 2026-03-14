class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self, iterable=None):
        self.head = None
        self._size = 0
        if iterable:
            for item in iterable:
                self.append(item)

    def append(self, x):
        new_node = Node(x)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self._size += 1

    def insert(self, i, x):
        if i < 0:
            i = max(0, self._size + i)
        i = min(i, self._size)
        new_node = Node(x)
        if i == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            cur = self.head
            for _ in range(i - 1):
                cur = cur.next
            new_node.next = cur.next
            cur.next = new_node
        self._size += 1

    def remove(self, x):
        if self.head is None:
            raise ValueError(f"{x}은(는) 리스트에 없습니다")
        if self.head.data == x:
            self.head = self.head.next
            self._size -= 1
            return
        cur = self.head
        while cur.next:
            if cur.next.data == x:
                cur.next = cur.next.next
                self._size -= 1
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
        if i == 0:
            val = self.head.data
            self.head = self.head.next
            self._size -= 1
            return val
        cur = self.head
        for _ in range(i - 1):
            cur = cur.next
        val = cur.next.data
        cur.next = cur.next.next
        self._size -= 1
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
        self._size = 0

    def __len__(self):
        return self._size

    def __getitem__(self, i):
        if i < 0:
            i = self._size + i
        if i < 0 or i >= self._size:
            raise IndexError("리스트 인덱스가 범위를 벗어났습니다")
        cur = self.head
        for _ in range(i):
            cur = cur.next
        return cur.data

    def __setitem__(self, i, x):
        if i < 0:
            i = self._size + i
        if i < 0 or i >= self._size:
            raise IndexError("리스트 할당 인덱스가 범위를 벗어났습니다")
        cur = self.head
        for _ in range(i):
            cur = cur.next
        cur.data = x

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
    ll = SinglyLinkedList([1, 2, 3])
    ll.insert(0, 0)
    print(ll)           # [0, 1, 2, 3]

    ll.remove(2)
    print(ll)           # [0, 1, 3]

    print(ll.pop())     # 3
    print(ll.pop(0))    # 0
    print(ll)           # [1]

    ll.extend([2, 3])
    print(ll)           # [1, 2, 3]
    print(ll[1])        # 2
    print(2 in ll)      # True
    print(ll.index(3))  # 2
    print(ll.count(2))  # 1
    print(len(ll))      # 3

    ll[0] = 9
    print(ll)           # [9, 2, 3]

    del ll[1]
    print(ll)           # [9, 3]

    ll.clear()
    print(ll)           # []
