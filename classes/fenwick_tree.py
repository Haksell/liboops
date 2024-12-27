from itertools import count
import random
import pytest


class FenwickTree:
    def __init__(self, size):
        self.__len = size
        self.__tree = [0] * (size + 1)
        self.__sum = 0
        self.__mid = 1 << (len(self.__tree).bit_length() - 1)

    @staticmethod
    def from_list(data):
        instance = FenwickTree(len(data))
        for i, n in enumerate(data, 1):
            instance.__tree[i] += n
            j = i + (i & -i)
            if j <= instance.__len:
                instance.__tree[j] += instance.__tree[i]
            instance.__sum += n
        return instance

    def __len__(self):
        return self.__len

    def __getitem__(self, i):
        return self.prefix_sum(i + 1) - self.prefix_sum(i)

    @property
    def sum(self):
        return self.__sum

    def update(self, i, delta):
        i += 1
        self.__sum += delta
        while i <= self.__len:
            self.__tree[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        res = 0
        while i > 0:
            res += self.__tree[i]
            i -= i & -i
        return res

    def suffix_sum(self, i):
        return self.__sum - self.prefix_sum(i)

    def range_sum(self, left, right):
        return self.prefix_sum(right) - self.prefix_sum(left)

    # Following methods require all elements to be nonnegative

    def nth(self, nth):
        if nth < 0 or nth >= self.__sum:
            return None
        i = self.__mid
        shift = i >> 1
        res = 0
        while True:
            if i > self.__len or self.__tree[i] > nth:
                i -= shift
            else:
                nth -= self.__tree[i]
                res = i
                i += shift
            if shift == 0:
                return res
            shift >>= 1

    def h_index(self):
        i = self.__mid
        shift = i >> 1
        res = 0
        bigger = self.__sum
        while True:
            if i > self.__len or bigger - self.__tree[i] < i:
                i -= shift
            else:
                bigger -= self.__tree[i]
                res = i
                i += shift
            if shift == 0:
                return res
            shift >>= 1


@pytest.mark.parametrize("repeats", range(100))
def test_fenwick_tree(repeats):
    n = random.randrange(100)
    if random.random() < 0.5:
        a = [random.randint(-100, 100) for _ in range(n)]
        fenwick_tree = FenwickTree.from_list(a)
    else:
        a = [0] * n
        fenwick_tree = FenwickTree(n)
    assert len(fenwick_tree) == n
    if n == 0:
        return
    for _ in range(random.randrange(100)):
        i = random.randrange(n)
        delta = random.randint(-100, 100)
        fenwick_tree.update(i, delta)
        a[i] += delta
        assert sum(a) == fenwick_tree.sum
        for j in range(n):
            assert fenwick_tree[j] == a[j]
            assert fenwick_tree.prefix_sum(j) == sum(a[:j])
            assert fenwick_tree.suffix_sum(j) == sum(a[j:])
        lo, hi = sorted(random.choices(range(n + 1), k=2))
        assert fenwick_tree.range_sum(lo, hi) == sum(a[lo:hi])


@pytest.mark.parametrize("repeats", range(42))
def test_fenwick_tree_nth(repeats):
    n = random.randrange(42)
    a = random.choices(range(42), k=n)
    fenwick_tree = FenwickTree.from_list(a)

    s = sum(a)
    nth = 0
    naive = [0] * s
    for i, ai in enumerate(a):
        for _ in range(ai):
            naive[nth] = i
            nth += 1

    assert fenwick_tree.nth(-1) is None
    assert fenwick_tree.nth(s) is None
    for nth in range(s):
        assert fenwick_tree.nth(nth) == naive[nth]


@pytest.mark.parametrize("repeats", range(42))
def test_fenwick_tree_h_index(repeats):
    def naive_h_index(a):
        for i in count(1):
            if sum(x >= i for x in a) < i:
                return i - 1

    n = random.randrange(1, 42)
    a = random.choices(range(n), k=random.randrange(42))
    fenwick_tree = FenwickTree(n)
    for x in a:
        fenwick_tree.update(x, 1)
    naive_res = naive_h_index(a)
    builtin_res = fenwick_tree.h_index()
    assert naive_res == builtin_res, (
        a,
        naive_res,
        builtin_res,
        (0, len(fenwick_tree) + 1),
        [(i, fenwick_tree.suffix_sum(i)) for i in range(n)],
    )


def test_fenwick_tree_h_index_zero():
    assert FenwickTree(0).h_index() == 0
    assert FenwickTree(1).h_index() == 0
    assert FenwickTree(2).h_index() == 0
    assert FenwickTree(3).h_index() == 0
    assert FenwickTree.from_list([]).h_index() == 0
    assert FenwickTree.from_list([0]).h_index() == 0
    assert FenwickTree.from_list([0, 0]).h_index() == 0
    assert FenwickTree.from_list([0, 0, 0]).h_index() == 0
