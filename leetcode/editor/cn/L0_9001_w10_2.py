import unittest


class AVLtreeTest:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, val: int) -> None:
        raise NotImplementedError

    def height(self) -> int:
        return -1

class TestAVLTree(unittest.TestCase):
    tree = AVLtreeTest()

    def test_height(self):
        self.tree.height()

    def test_insert(self):
        self.tree.insert()