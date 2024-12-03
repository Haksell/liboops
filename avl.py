# TODO: separate AVLMultiset, AVLSet and AVLMap


class AVL:
    class Node:
        def __init__(self, key):
            self.key = key
            self.height = 1
            self.count = 1
            self.left = self.right = None
            self.left_count = self.right_count = 0

        def _update_and_balance(self):
            self.left_count = AVL._get_size(self.left)
            self.right_count = AVL._get_size(self.right)
            self.height = 1 + max(
                AVL._get_height(self.left), AVL._get_height(self.right)
            )

            balance = AVL._get_balance(self)
            balance_left = AVL._get_balance(self.left)
            balance_right = AVL._get_balance(self.right)

            if balance > 1:
                # Left Left Case
                if balance_left >= 0:
                    return self.AVL._rotate_right()
                # Left Right Case
                else:
                    self.left = self.left._rotate_left()
                    return self.AVL._rotate_right()
            elif balance < -1:
                # Right Right Case
                if balance_right <= 0:
                    return self._rotate_left()
                # Right Left Case
                else:
                    self.right = self.right._rotate_right()
                    return self._rotate_left()

            return self

        def _rotate_left(self):
            y = self.right
            x = y.left

            y.left = self
            self.right = x

            self.left_count = AVL._get_size(self.left)
            self.right_count = AVL._get_size(self.right)
            y.left_count = AVL._get_size(y.left)
            y.right_count = AVL._get_size(y.right)

            self.height = 1 + max(
                AVL._get_height(self.left), AVL._get_height(self.right)
            )
            y.height = 1 + max(AVL._get_height(y.left), AVL._get_height(y.right))

            return y

        def _rotate_right(self):
            x = self.left
            z = x.right

            x.right = self
            self.left = z

            self.left_count = AVL._get_size(self.left)
            self.right_count = AVL._get_size(self.right)
            x.left_count = AVL._get_size(x.left)
            x.right_count = AVL._get_size(x.right)

            self.height = 1 + max(
                AVL._get_height(self.left), AVL._get_height(self.right)
            )
            x.height = 1 + max(AVL._get_height(x.left), AVL._get_height(x.right))

            return x

    def __init__(self):
        self.root = None

    def __len__(self):
        root = self.root
        return root.left_count + root.count + root.right_count if root else 0

    def __repr__(self):
        def inorder(node, depth):
            return (
                inorder(node.left, depth + 1)
                + [
                    "  " * depth
                    + f"{node.key}: {node.left_count} < {node.count} > {node.right_count}"
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

    @staticmethod
    def _get_height(node):
        return node.height if node else 0

    @staticmethod
    def _get_size(node):
        return node.left_count + node.count + node.right_count if node else 0

    @staticmethod
    def _get_balance(node):
        return AVL._get_height(node.left) - AVL._get_height(node.right) if node else 0

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
