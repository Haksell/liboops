# TODO: separate AVLMultiset, AVLSet and AVLMap


class AVL:
    class Node:
        def __init__(self, key):
            self.key = key
            self.height = 1
            self.count = 1
            self.left = self.right = None
            self.left_size = self.right_size = 0

        @property
        def size(self):
            return self.left_size + self.count + self.right_size

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
            self.left_size = self.left.size if self.left else 0
            self.right_size = self.right.size if self.right else 0
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
        root = self.root
        return root.left_size + root.count + root.right_size if root else 0

    def __repr__(self):
        def inorder(node, depth):
            return (
                inorder(node.left, depth + 1)
                + [
                    "  " * depth
                    + f"{node.key}: {node.left_size} < {node.count} > {node.right_size}"
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
            # find successor
            tmp = node.right
            while tmp.left is not None:
                tmp = tmp.left
            node.key = tmp.key
            node.count = tmp.count
            # TODO: no recursive call, just remember parent
            tmp.count = 1  # reset tmp count to 1 to delete it ???
            node.right = self.__delete(node.right, tmp.key)
        return node._update_and_balance()


if __name__ == "__main__":
    avl_tree = AVL()
    data = [10, 20, 20, 30, 40, 50, 25, 20]
    for num in data:
        avl_tree.insert(num)

    print("Inorder traversal after insertions:")
    print(avl_tree)

    for dk in [20, 30, 10, 20, 20]:
        avl_tree.delete(dk)
        print(f"\nInorder traversal after deleting {dk}:")
        print(avl_tree)
