# TODO: separate AVLMultiset, AVLSet and AVLMap


class AVL:
    class Node:
        def __init__(self, key):
            self.key = key
            self.height = 1
            self.count = 1
            self.left = self.right = None
            self.left_count = self.right_count = 0

        def update(self):
            self.left_count = AVL._get_size(self.left)
            self.right_count = AVL._get_size(self.right)
            self.height = 1 + max(
                AVL._get_height(self.left), AVL._get_height(self.right)
            )

    def __init__(self):
        self.root = None

    def __len__(self):
        root = self.root
        return root.left_count + root.count + root.right_count if root else 0

    @staticmethod
    def _get_height(node):
        return node.height if node else 0

    @staticmethod
    def _get_size(node):
        return node.left_count + node.count + node.right_count if node else 0

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

        return self.__update_and_balance(node)

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

        return self.__update_and_balance(node)

    def __get_balance(self, node):
        return AVL._get_height(node.left) - AVL._get_height(node.right) if node else 0

    def __update_and_balance(self, node):
        node.update()
        balance = self.__get_balance(node)

        # Left Left Case
        if balance > 1 and self.__get_balance(node.left) >= 0:
            return self.__rotate_right(node)
        # Left Right Case
        if balance > 1 and self.__get_balance(node.left) < 0:
            node.left = self.__rotate_left(node.left)
            return self.__rotate_right(node)
        # Right Right Case
        if balance < -1 and self.__get_balance(node.right) <= 0:
            return self.__rotate_left(node)
        # Right Left Case
        if balance < -1 and self.__get_balance(node.right) > 0:
            node.right = self.__rotate_right(node.right)
            return self.__rotate_left(node)

        return node

    def __rotate_left(self, z):
        y = z.right
        x = y.left

        y.left = z
        z.right = x

        z.left_count = AVL._get_size(z.left)
        z.right_count = AVL._get_size(z.right)
        y.left_count = AVL._get_size(y.left)
        y.right_count = AVL._get_size(y.right)

        z.height = 1 + max(AVL._get_height(z.left), AVL._get_height(z.right))
        y.height = 1 + max(AVL._get_height(y.left), AVL._get_height(y.right))

        return y

    def __rotate_right(self, y):
        x = y.left
        z = x.right

        x.right = y
        y.left = z

        y.left_count = AVL._get_size(y.left)
        y.right_count = AVL._get_size(y.right)
        x.left_count = AVL._get_size(x.left)
        x.right_count = AVL._get_size(x.right)

        y.height = 1 + max(AVL._get_height(y.left), AVL._get_height(y.right))
        x.height = 1 + max(AVL._get_height(x.left), AVL._get_height(x.right))

        return x

    def __print_inorder(self, node, depth):
        if not node:
            return
        self.__print_inorder(node.left, depth + 1)
        print(
            "  " * depth
            + f"{node.key}: {node.left_count} < {node.count} > {node.right_count}"
        )
        self.__print_inorder(node.right, depth + 1)

    def print_inorder(self):
        if self.root:
            self.__print_inorder(self.root, 0)
        else:
            print(f"{self.__class__.__name__}()")


if __name__ == "__main__":
    avl_tree = AVL()
    data = [10, 20, 20, 30, 40, 50, 25, 20]
    for num in data:
        avl_tree.insert(num)

    print("Inorder traversal after insertions:")
    avl_tree.print_inorder()

    for dk in [20, 30, 10, 20, 20]:
        avl_tree.delete(dk)
        print(f"\nInorder traversal after deleting {dk}:")
        avl_tree.print_inorder()
