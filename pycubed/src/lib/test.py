from collections import deque

class A:

    def __init__(self, q):
        self.q = q

class B:

    def __init__(self, q):
        self.q = q

if __name__ == "__main__":
    q = deque([1, 2, 3])
    a = A(q)
    b = B(q)
    a.q.popleft()
    a.q.popleft()
    a.q.popleft()
    print(b.q)