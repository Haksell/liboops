# TODO: separate AVLMultiSet, AVLSet and AVLMap


from collections import Counter


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

    def __len__(self):
        return len(self.root) if self.root else 0

    def __contains__(self, key):
        return key in self.root if self.root else False

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


def test_avl_insert():
    avl = AVLMultiSet()
    keys = [10, 20, 30, 40, 50, 25]
    for key in keys:
        avl.insert(key)
    assert len(avl) == len(keys)
    # Test the balance of the tree
    assert avl.root.balance in [-1, 0, 1]


def test_avl_delete_leaf():
    avl = AVLMultiSet()
    keys = [20, 10, 30]
    for key in keys:
        avl.insert(key)
    avl.delete(10)
    assert len(avl) == 2
    assert avl.root.left is None


def test_avl_delete_node_with_one_child():
    avl = AVLMultiSet()
    keys = [20, 10, 30, 25]
    for key in keys:
        avl.insert(key)
    avl.delete(30)
    assert len(avl) == 3
    assert avl.root.right.key == 25


def test_avl_delete_node_with_two_children():
    avl = AVLMultiSet()
    keys = [50, 30, 70, 20, 40, 60, 80]
    for key in keys:
        avl.insert(key)
    avl.delete(50)
    assert len(avl) == 6
    assert avl.root.key != 50
    # Ensure the tree is balanced
    assert avl.root.balance in [-1, 0, 1]


def test_avl_duplicate_keys():
    avl = AVLMultiSet()
    keys = [10, 20, 20, 30, 30, 30]
    for key in keys:
        avl.insert(key)
    assert len(avl) == len(keys)
    avl.delete(20)
    assert len(avl) == 5
    avl.delete(20)
    assert len(avl) == 4
    # Deleting 20 again should remove it completely
    avl.delete(20)
    assert len(avl) == 4  # No change, 20 was already removed


def test_avl_height():
    avl = AVLMultiSet()
    keys = [10, 20, 30, 40, 50, 25]
    for key in keys:
        avl.insert(key)
    # For an AVL tree, the height should be minimal (logarithmic)
    assert avl.root.height == 3


def test_avl_left_right_rotations():
    avl = AVLMultiSet()
    avl.insert(30)
    avl.insert(20)
    avl.insert(10)  # Should cause a right rotation
    assert avl.root.key == 20
    avl = AVLMultiSet()
    avl.insert(10)
    avl.insert(20)
    avl.insert(30)  # Should cause a left rotation
    assert avl.root.key == 20


def test_avl_complex_operations():
    avl = AVLMultiSet()
    operations = [
        ("insert", 10),
        ("insert", 20),
        ("insert", 30),
        ("delete", 20),
        ("insert", 25),
        ("insert", 5),
        ("delete", 10),
        ("insert", 15),
    ]
    for op, key in operations:
        if op == "insert":
            avl.insert(key)
        elif op == "delete":
            avl.delete(key)
    assert len(avl) == 4
    # Ensure the tree is balanced after complex operations
    assert avl.root.balance in [-1, 0, 1]


def test_avl_multiset():
    for _ in range(100):
        keys = []
        cnt = Counter()
        avl = AVLMultiSet()
        # for _ in range(100):
        #     if


if __name__ == "__main__":
    avl = AVLMultiSet()
    print(bool(avl))
    data = [10, 20, 20, 30, 40, 50, 25, 20]
    for num in data:
        avl.insert(num)
    print(bool(avl))

    print("Inorder traversal after insertions:")
    print(avl)

    for dk in [20, 30, 10, 20, 20]:
        avl.delete(dk)
        print(f"\nInorder traversal after deleting {dk}:")
        print(avl)
