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
            self.count = 1
            self.left = self.right = None
            self.left_len = self.right_len = 0

        def __len__(self):
            return self.left_len + self.count + self.right_len

        def __contains__(self, key):
            if key < self.key:
                return key in self.left if self.left else False
            elif key > self.key:
                return key in self.right if self.right else False
            else:
                return True

        def __iter__(self):
            if self.left:
                yield from self.left
            for _ in range(self.count):
                yield self.key
            if self.right:
                yield from self.right

        @property
        def left_height(self):
            return self.left.height if self.left else 0

        @property
        def right_height(self):
            return self.right.height if self.right else 0

        @property
        def balance(self):
            return self.left_height - self.right_height

        def _update(self):
            self.left_len = len(self.left) if self.left else 0
            self.right_len = len(self.right) if self.right else 0
            self.height = 1 + max(self.left_height, self.right_height)

        def _update_and_balance(self):
            self._update()
            balance = self.balance
            if balance > 1:
                if self.left and self.left.balance >= 0:  # Left Left
                    return self._rotate_right()
                else:  # Left Right
                    self.left = self.left._rotate_left()
                    return self._rotate_right()
            elif balance < -1:
                if self.right and self.right.balance <= 0:  # Right Right
                    return self._rotate_left()
                else:  # Right Left
                    self.right = self.right._rotate_right()
                    return self._rotate_left()
            else:
                return self

        def _rotate_left(self):
            # TODO: with tuple unpacking
            parent = self.right
            sibling = parent.left

            parent.left = self
            self.right = sibling

            self._update()
            parent._update()
            return parent

        def _rotate_right(self):
            # TODO: with tuple unpacking
            parent = self.left
            sibling = parent.right
            parent.right = self
            self.left = sibling
            self._update()
            parent._update()
            return parent

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

    def __repr__(self):
        def inorder(node, depth):
            return (
                inorder(node.left, depth + 1)
                + [
                    "  " * depth
                    + f"{node.key}: {node.left_len} < {node.count} > {node.right_len}"
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
        self.root = self.__insert(self.root, key)

    def __insert(self, node, key):
        if node is None:
            return self.Node(key)
        if key == node.key:
            node.count += 1
            return node
        if key < node.key:
            node.left = self.__insert(node.left, key)
        else:
            node.right = self.__insert(node.right, key)
        return node._update_and_balance()

    def delete(self, key):
        self.root = self.__delete(self.root, key)

    def __delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self.__delete(node.left, key)
        elif key > node.key:
            node.right = self.__delete(node.right, key)
        elif node.count > 1:
            node.count -= 1
            return node
        elif node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key = successor.key
            node.count = successor.count
            successor.count = 1  # reset successor count to 1 to delete it
            node.right = self.__delete(node.right, successor.key)
        return node._update_and_balance()


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
            avl_cnt[node.key] = node.count
            fill(node.right)

        avl_cnt = Counter()
        fill(avl)
        return avl_cnt == true_cnt

    lo, hi = sorted(random.choices(range(-100, 101), k=2))
    cnt = Counter()
    avl = AVLMultiSet()
    for _ in range(100):
        if cnt and random.random() < 0.4:
            key = random.choice(list(cnt.keys()))
            avl.delete(key)
            if cnt[key] == 1:
                del cnt[key]
            else:
                cnt[key] -= 1
        else:
            key = random.randint(lo, hi)
            avl.insert(key)
            cnt[key] += 1
        assert is_sorted(avl.root)
        assert is_balanced(avl.root)
        assert matches(avl.root, cnt)
        for i in range(lo, hi + 1):
            assert (i in avl) == (i in cnt)
        data = list(avl)
        assert all(map(int.__le__, data, data[1:]))
        assert Counter(data) == cnt
        assert len(data) == sum(cnt.values())
