import unittest


class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, val: int) -> None:
        return 1

    def height(self) -> int:
        return -1


class TestAVLTree(unittest.TestCase):

    def setUp(self):
        # 每个 test_ 方法开始前，自动创建一棵新树
        self.tree = AVLTree()

    def test_empty_tree_height(self):
        actual_height = self.tree.height()

        # 假设我们规定：空树高度是 -1
        self.assertEqual(actual_height, -1)

    def test_insert(self):
        self.tree.insert(10)

        self.assertEqual(self.tree.size, 0)

    def test_insert2(self):
        self.tree.insert(10)

        self.assertEqual(self.tree.size, 0)
if __name__ == "__main__":
    unittest.main(verbosity=2)