# TODO: separate AVLMultiset, AVLSet and AVLMap


class AVL:
    class Node:
        def __init__(self, key):
            self.key = key
            self.height = 1
            self.count = 1
            self.left = self.right = None
            self.left_size = self.right_size = 0

        @staticmethod
        def _get_height(node):
            return node.height if node else 0

        @property
        def size(self):
            return self.left_size + self.count + self.right_size

        @staticmethod
        def _get_size(node):
            return node.size if node else 0

        @property
        def balance(self):
            return AVL.Node._get_height(self.left) - AVL.Node._get_height(self.right)

        @staticmethod
        def _get_balance(node):
            return node.balance if node else 0

        def _update_height(self):
            self.height = 1 + max(
                AVL.Node._get_height(self.left), AVL.Node._get_height(self.right)
            )

        def _update_and_balance(self):
            self.left_size = AVL.Node._get_size(self.left)
            self.right_size = AVL.Node._get_size(self.right)
            self._update_height()

            balance = self.balance

            if balance > 1:
                if AVL.Node._get_balance(self.left) >= 0:  # Left Left Case
                    return self._rotate_right()
                else:  # Left Right Case
                    self.left = self.left._rotate_left()
                    return self._rotate_right()
            elif balance < -1:
                if AVL.Node._get_balance(self.right) <= 0:  # Right Right Case
                    return self._rotate_left()
                else:  # Right Left Case
                    self.right = self.right._rotate_right()
                    return self._rotate_left()
            else:
                return self

        def _rotate_left(self):
            parent = self.right
            sibling = parent.left

            parent.left = self
            self.right = sibling

            self.left_size = AVL.Node._get_size(self.left)
            self.right_size = AVL.Node._get_size(self.right)
            parent.left_size = AVL.Node._get_size(parent.left)
            parent.right_size = AVL.Node._get_size(parent.right)

            self._update_height()
            parent._update_height()

            return parent

        def _rotate_right(self):
            parent = self.left
            sibling = parent.right

            parent.right = self
            self.left = sibling

            self.left_size = AVL.Node._get_size(self.left)
            self.right_size = AVL.Node._get_size(self.right)
            parent.left_size = AVL.Node._get_size(parent.left)
            parent.right_size = AVL.Node._get_size(parent.right)

            self._update_height()
            parent._update_height()

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
            if node is None:
                return None

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
