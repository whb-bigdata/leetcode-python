"""Common operations for a binary search tree.

The tree stores comparable values. Inserting the same value more than once
keeps a single node for that value.
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Generic, List, Optional, TypeVar


T = TypeVar("T")


class TreeNode(Generic[T]):
    """A node in a binary tree."""

    def __init__(self, value: T) -> None:
        self.value = value
        self.left: Optional[TreeNode[T]] = None
        self.right: Optional[TreeNode[T]] = None


class BinarySearchTree(Generic[T]):
    """A binary search tree with common traversal and query operations."""

    def __init__(self) -> None:
        self.root: Optional[TreeNode[T]] = None
        self._size = 0

    def insert(self, value: T) -> TreeNode[T]:
        """Insert ``value`` and return its node.

        Values smaller than a node are placed on its left; larger values are
        placed on its right. If the value already exists, its existing node is
        returned without changing the tree.
        """
        if self.root is None:
            self.root = TreeNode(value)
            self._size = 1
            return self.root

        current = self.root
        while True:
            if value == current.value:
                return current
            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    self._size += 1
                    return current.left
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(value)
                    self._size += 1
                    return current.right
                current = current.right

    def find(self, value: T) -> Optional[TreeNode[T]]:
        """Return the node containing ``value``, or ``None`` if absent."""
        current = self.root
        while current is not None:
            if value == current.value:
                return current
            current = current.left if value < current.value else current.right
        return None

    def preorder(self) -> List[T]:
        """Return values in preorder: root, left subtree, right subtree."""
        values: List[T] = []

        def visit(node: Optional[TreeNode[T]]) -> None:
            if node is None:
                return
            values.append(node.value)
            visit(node.left)
            visit(node.right)

        visit(self.root)
        return values

    def inorder(self) -> List[T]:
        """Return values in inorder: left subtree, root, right subtree."""
        values: List[T] = []

        def visit(node: Optional[TreeNode[T]]) -> None:
            if node is None:
                return
            visit(node.left)
            values.append(node.value)
            visit(node.right)

        visit(self.root)
        return values

    def postorder(self) -> List[T]:
        """Return values in postorder: left subtree, right subtree, root."""
        values: List[T] = []

        def visit(node: Optional[TreeNode[T]]) -> None:
            if node is None:
                return
            visit(node.left)
            visit(node.right)
            values.append(node.value)

        visit(self.root)
        return values

    def level_order(self) -> List[T]:
        """Return values level by level, from left to right."""
        if self.root is None:
            return []

        values: List[T] = []
        queue: Deque[TreeNode[T]] = deque([self.root])
        while queue:
            node = queue.popleft()
            values.append(node.value)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return values

    def height(self) -> int:
        """Return the tree height measured as the number of node levels."""
        def measure(node: Optional[TreeNode[T]]) -> int:
            if node is None:
                return 0
            return 1 + max(measure(node.left), measure(node.right))

        return measure(self.root)

    def leaf_count(self) -> int:
        """Return the number of nodes with no left or right child."""
        def count(node: Optional[TreeNode[T]]) -> int:
            if node is None:
                return 0
            if node.left is None and node.right is None:
                return 1
            return count(node.left) + count(node.right)

        return count(self.root)

    def size(self) -> int:
        """Return the total number of nodes in the tree."""
        return self._size

    def is_empty(self) -> bool:
        """Return whether the tree contains no nodes."""
        return self.root is None

    def clear(self) -> None:
        """Remove every node from the tree."""
        self.root = None
        self._size = 0


if __name__ == "__main__":
    tree = BinarySearchTree[int]()
    for number in (8, 3, 10, 1, 6, 14, 4, 7, 13):
        tree.insert(number)

    print("Preorder:", tree.preorder())
    print("Inorder:", tree.inorder())
    print("Postorder:", tree.postorder())
    print("Level order:", tree.level_order())
    print("Height:", tree.height())
    print("Leaf count:", tree.leaf_count())
