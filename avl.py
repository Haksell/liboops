# TODO: separate AVLMultiSet, AVLSet and AVLMap


from collections import Counter
from math import inf as INF
import pytest
import random


class AVLMultiSet:
    class Node:
        def __init__(self, key):
            self.key = key
            self.height = 1
            self.freq = 1
            self.left = self.right = None
            self.left_len = self.right_len = 0

        def __len__(self):
            return self.left_len + self.freq + self.right_len

        def __iter__(self):
            if self.left:
                yield from self.left
            for _ in range(self.freq):
                yield self.key
            if self.right:
                yield from self.right

        def __contains__(self, key):
            return self.count(key) >= 1

        def __getitem__(self, idx):
            if idx < self.left_len:
                return self.left[idx]
            elif idx < self.left_len + self.freq:
                return self.key
            else:
                return self.right[idx - self.left_len - self.freq]

        @property
        def left_height(self):
            return self.left.height if self.left else 0

        @property
        def right_height(self):
            return self.right.height if self.right else 0

        @property
        def balance(self):
            return self.left_height - self.right_height

        def delete(self, key):
            if key < self.key:
                self.left = self.left.delete(key)
            elif key > self.key:
                self.right = self.right.delete(key)
            elif self.freq > 1:
                self.freq -= 1
                return self
            elif self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            else:
                successor = self.right
                while successor.left is not None:
                    successor = successor.left
                self.key = successor.key
                self.freq = successor.freq
                successor.freq = 1  # reset successor count to 1 to delete it
                self.right = self.right.delete(successor.key)
            return self.__update_and_balance()

        def insert(self, key):
            if self is None:
                return AVLMultiSet.Node(key)
            if key == self.key:
                self.freq += 1
                return self
            if key < self.key:
                self.left = (
                    self.left.insert(key) if self.left else AVLMultiSet.Node(key)
                )
            else:
                self.right = (
                    self.right.insert(key) if self.right else AVLMultiSet.Node(key)
                )
            return self.__update_and_balance()

        def __update_and_balance(self):
            self.__update()
            balance = self.balance
            if balance > 1:
                if self.left and self.left.balance >= 0:  # Left Left
                    return self.__rotate_right()
                else:  # Left Right
                    self.left = self.left.__rotate_left()
                    return self.__rotate_right()
            elif balance < -1:
                if self.right and self.right.balance <= 0:  # Right Right
                    return self.__rotate_left()
                else:  # Right Left
                    self.right = self.right.__rotate_right()
                    return self.__rotate_left()
            else:
                return self

        def __update(self):
            self.left_len = len(self.left) if self.left else 0
            self.right_len = len(self.right) if self.right else 0
            self.height = 1 + max(self.left_height, self.right_height)

        def __rotate_left(self):
            parent, self.right.left, self.right = self.right, self, self.right.left
            self.__update()
            parent.__update()
            return parent

        def __rotate_right(self):
            parent, self.left.right, self.left = self.left, self, self.left.right
            self.__update()
            parent.__update()
            return parent

        def count(self, key):
            if key < self.key:
                return self.left.count(key) if self.left else 0
            elif key > self.key:
                return self.right.count(key) if self.right else 0
            else:
                return self.freq

        def unique(self):
            if self.left:
                yield from self.left.unique()
            yield self.key
            if self.right:
                yield from self.right.unique()

    def __init__(self):
        self.root = None

    def __bool__(self):
        return self.root is not None

    def __len__(self):
        return len(self.root) if self.root else 0

    def __contains__(self, key):
        return key in self.root if self.root else False

    def __iter__(self):
        if self.root is None:
            return
        yield from self.root

    def __getitem__(self, idx):
        if idx >= len(self) or idx < -len(self):
            raise IndexError(f"{self.__class__.__name__} index out of range")
        return self.root[idx] if idx >= 0 else self.root[idx + len(self.root)]

    def __repr__(self):
        def inorder(node, depth):
            return (
                inorder(node.left, depth + 1)
                + [
                    "  " * depth
                    + f"{node.key}: {node.left_len} < {node.freq} > {node.right_len}"
                ]
                + inorder(node.right, depth + 1)
                if node
                else []
            )

        return (
            "\n".join(inorder(self.root, 0))
            if self.root
            else f"{self.__class__.__name__}()"
        )

    def insert(self, key):
        self.root = self.root.insert(key) if self.root else AVLMultiSet.Node(key)

    def delete(self, key):
        self.root = self.root and self.root.delete(key)

    def count(self, key):
        return self.root.count(key) if self.root else 0

    def unique(self):
        if self.root is None:
            return
        yield from self.root.unique()

    def smaller_than(self, key):
        res = 0
        node = self.root
        while node:
            if node.key >= key:
                node = node.left
            else:
                res += node.freq + node.left_len
                node = node.right
        return res


@pytest.mark.parametrize("repeats", range(100))
def test_avl_multiset(repeats):
    def is_sorted(avl, lo=-INF, hi=INF):
        return avl is None or (
            avl.key > lo
            and avl.key < hi
            and is_sorted(avl.left, lo, avl.key)
            and is_sorted(avl.right, avl.key, hi)
        )

    def is_balanced(avl):
        return avl is None or (
            -1 <= avl.balance <= 1 and is_balanced(avl.left) and is_balanced(avl.right)
        )

    def matches(avl, true_cnt):
        def fill(node):
            if node is None:
                return
            fill(node.left)
            avl_cnt[node.key] = node.freq
            fill(node.right)

        avl_cnt = Counter()
        fill(avl)
        return avl_cnt == true_cnt

    lo, hi = sorted(random.choices(range(-100, 101), k=2))
    cnt = Counter()
    avl = AVLMultiSet()
    for _ in range(random.randrange(100)):
        if cnt and random.random() < 0.4:
            key = random.choice(list(cnt.keys()))
            deletions = random.randint(1, cnt[key])
            for _ in range(deletions):
                avl.delete(key)
            if cnt[key] == deletions:
                del cnt[key]
            else:
                cnt[key] -= deletions
        else:
            key = random.randint(lo, hi)
            insertions = random.randint(1, 3)
            for _ in range(insertions):
                avl.insert(key)
            cnt[key] += insertions
        assert is_sorted(avl.root)
        assert is_balanced(avl.root)
        assert matches(avl.root, cnt)
        for i in range(lo, hi + 1):
            assert (i in avl) == (i in cnt)
            assert avl.count(i) == cnt[i]
        data = list(avl)
        assert all(map(int.__le__, data, data[1:]))
        assert Counter(data) == cnt
        assert len(data) == len(avl) == sum(cnt.values())
        assert list(avl.unique()) == sorted(set(data))
        for i in range(len(avl)):
            assert avl[i] == data[i]
            assert avl[~i] == data[~i]
        cmp_key = random.randint(lo, hi)
        assert avl.smaller_than(cmp_key) == sum(x < cmp_key for x in data)
