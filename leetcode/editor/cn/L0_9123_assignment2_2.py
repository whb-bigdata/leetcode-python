"""COMP9123 Assignment 2, Question 2: AVL-tree double-ended priority queue.

The AVL tree stores unique integer keys. In addition to the root, the DEPQ
keeps direct references to its smallest and largest nodes. Therefore finding
either extreme is O(1), while AVL insertion and deletion remain O(log n).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class _AVLNode:
    key: int
    left: Optional["_AVLNode"] = None
    right: Optional["_AVLNode"] = None
    height: int = 1


class AVLDoubleEndedPriorityQueue:
    """A double-ended priority queue backed by an AVL search tree."""

    def __init__(self) -> None:
        self._root: Optional[_AVLNode] = None
        self._min_node: Optional[_AVLNode] = None
        self._max_node: Optional[_AVLNode] = None
        self._size = 0

    def insert(self, key: int) -> None:
        """Insert a unique key in O(log n) time.

        The recursive insert and any required AVL rotations preserve the binary
        search-tree and balance invariants. Rotations preserve key order, so
        they cannot change which key is globally smallest or largest.
        """
        if self._find_node(key) is not None:
            raise ValueError("duplicate keys are not supported")

        self._root = self._insert(self._root, key)
        self._size += 1
        if self._min_node is None or key < self._min_node.key:
            self._min_node = self._find_node(key)
        if self._max_node is None or key > self._max_node.key:
            self._max_node = self._find_node(key)

    def find_min(self) -> int:
        """Return the smallest key in O(1) time without removing it."""
        if self._min_node is None:
            raise IndexError("find_min from an empty DEPQ")
        return self._min_node.key

    def find_max(self) -> int:
        """Return the largest key in O(1) time without removing it."""
        if self._max_node is None:
            raise IndexError("find_max from an empty DEPQ")
        return self._max_node.key

    def remove_min(self) -> int:
        """Remove and return the smallest key in O(log n) time."""
        minimum = self.find_min()
        self._root = self._delete(self._root, minimum)
        self._size -= 1
        self._min_node = self._leftmost(self._root)
        self._max_node = self._rightmost(self._root)
        return minimum

    def remove_max(self) -> int:
        """Remove and return the largest key in O(log n) time."""
        maximum = self.find_max()
        self._root = self._delete(self._root, maximum)
        self._size -= 1
        self._min_node = self._leftmost(self._root)
        self._max_node = self._rightmost(self._root)
        return maximum

    def size(self) -> int:
        """Return the number of stored keys in O(1) time."""
        return self._size

    def is_empty(self) -> bool:
        """Return whether the DEPQ is empty in O(1) time."""
        return self._size == 0

    def inorder(self) -> List[int]:
        """Return the keys in ascending order, for demonstration and testing."""
        values: List[int] = []

        def visit(node: Optional[_AVLNode]) -> None:
            if node is not None:
                visit(node.left)
                values.append(node.key)
                visit(node.right)

        visit(self._root)
        return values

    def _insert(self, node: Optional[_AVLNode], key: int) -> _AVLNode:
        if node is None:
            return _AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return self._rebalance(node)

    def _delete(self, node: Optional[_AVLNode], key: int) -> Optional[_AVLNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        elif node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            successor = self._leftmost(node.right)
            assert successor is not None
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)
        return self._rebalance(node)

    def _find_node(self, key: int) -> Optional[_AVLNode]:
        node = self._root
        while node is not None:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    @staticmethod
    def _height(node: Optional[_AVLNode]) -> int:
        return node.height if node is not None else 0

    def _rebalance(self, node: _AVLNode) -> _AVLNode:
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._height(node.left) - self._height(node.right)

        if balance > 1:
            if self._height(node.left.left) < self._height(node.left.right):
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._height(node.right.right) < self._height(node.right.left):
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _rotate_left(self, node: _AVLNode) -> _AVLNode:
        pivot = node.right
        assert pivot is not None
        node.right = pivot.left
        pivot.left = node
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        pivot.height = 1 + max(self._height(pivot.left), self._height(pivot.right))
        return pivot

    def _rotate_right(self, node: _AVLNode) -> _AVLNode:
        pivot = node.left
        assert pivot is not None
        node.left = pivot.right
        pivot.right = node
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        pivot.height = 1 + max(self._height(pivot.left), self._height(pivot.right))
        return pivot

    @staticmethod
    def _leftmost(node: Optional[_AVLNode]) -> Optional[_AVLNode]:
        while node is not None and node.left is not None:
            node = node.left
        return node

    @staticmethod
    def _rightmost(node: Optional[_AVLNode]) -> Optional[_AVLNode]:
        while node is not None and node.right is not None:
            node = node.right
        return node


if __name__ == "__main__":
    depq = AVLDoubleEndedPriorityQueue()
    for key in (30, 10, 40, 5, 20, 35, 50, 15, 25):
        depq.insert(key)

    assert depq.inorder() == [5, 10, 15, 20, 25, 30, 35, 40, 50]
    assert depq.find_min() == 5
    assert depq.find_max() == 50
    assert depq.remove_min() == 5
    assert depq.remove_max() == 50
    assert depq.find_min() == 10
    assert depq.find_max() == 40
    print("DEPQ contents:", depq.inorder())
    print("AVL DEPQ checks passed.")
