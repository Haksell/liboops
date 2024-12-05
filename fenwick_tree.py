import random
import pytest


class FenwickTree:
    def __init__(self, size):
        self.__len = size
        self.__tree = [0] * (size + 1)

    @staticmethod
    def from_list(data):
        instance = FenwickTree(len(data))
        for i, n in enumerate(data, 1):
            instance.__tree[i] += n
            j = i + (i & -i)
            if j <= instance.__len:
                instance.__tree[j] += instance.__tree[i]
        return instance

    def __len__(self):
        return self.__len

    def update(self, i, delta):
        i += 1
        while i <= self.__len:
            self.__tree[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        res = 0
        while i > 0:
            res += self.__tree[i]
            i -= i & -i
        return res

    def range_sum(self, left, right):
        return self.prefix_sum(right) - self.prefix_sum(left)

    # TODO: nth_value using binary search


@pytest.mark.parametrize("repeats", range(100))
def test_fenwick_tree(repeats):
    n = random.randint(1, 100)
    if random.random() < 0.5:
        a = [random.randint(-100, 100) for _ in range(n)]
        fenwick_tree = FenwickTree.from_list(a)
    else:
        a = [0] * n
        fenwick_tree = FenwickTree(n)
    assert len(fenwick_tree) == n
    for _ in range(random.randrange(100)):
        i = random.randrange(n)
        delta = random.randint(-100, 100)
        fenwick_tree.update(i, delta)
        a[i] += delta
        for j in range(n):
            assert fenwick_tree.prefix_sum(j) == sum(a[:j])
        lo, hi = sorted(random.choices(range(n + 1), k=2))
        assert fenwick_tree.range_sum(lo, hi) == sum(a[lo:hi])
