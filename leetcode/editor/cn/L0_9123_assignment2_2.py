"""COMP9123 Assignment 2, Question 2: AVL-tree double-ended priority queue.

The AVL tree stores unique integer keys. In addition to the root, the DEPQ
keeps direct references to its smallest and largest nodes. Therefore finding
either extreme is O(1), while AVL insertion and deletion remain O(log n).

设计与中文回答一致：父指针支持迭代回溯，min/max 指针支持直接查询。
全局最小节点没有左孩子；AVL 平衡意味着其右孩子（若有）只能是叶子。
因此下一最小节点是其右孩子，或在无右孩子时是其父节点。最大值对称。
删除极值时直接摘除节点并接上唯一孩子，不复制键值，保留其他节点身份。

The five DEPQ operations use O(1) auxiliary space: rebalancing is iterative.
The tree uses O(n) total space. The optional inorder() diagnostic uses O(n)
output space and O(log n) recursion space; it is not a DEPQ operation.
Empty queries/removals raise IndexError; duplicate insertion raises ValueError.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(eq=False)
class _AVLNode:
    key: int
    left: Optional["_AVLNode"] = None
    right: Optional["_AVLNode"] = None
    height: int = 1
    parent: Optional["_AVLNode"] = None


class AVLDoubleEndedPriorityQueue:
    """A double-ended priority queue backed by an AVL search tree."""

    def __init__(self) -> None:
        self._root: Optional[_AVLNode] = None
        self._min_node: Optional[_AVLNode] = None
        self._max_node: Optional[_AVLNode] = None
        self._size = 0

    def insert(self, key: int) -> None:
        """Insert a unique key in O(log n) time.

        Search once and retain the inserted node reference. Rotations change
        links, not keys or node identities, so cached extrema remain valid.
        """
        parent = None
        node = self._root
        while node is not None:
            parent = node
            if key == node.key:
                raise ValueError("duplicate keys are not supported")
            node = node.left if key < node.key else node.right

        inserted = _AVLNode(key, parent=parent)
        if parent is None:
            self._root = inserted
        elif key < parent.key:
            parent.left = inserted
        else:
            parent.right = inserted

        self._size += 1
        if self._min_node is None or key < self._min_node.key:
            self._min_node = inserted
        if self._max_node is None or key > self._max_node.key:
            self._max_node = inserted
        self._rebalance_upwards(parent)

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
        minimum = self.find_min()  # Raises before changing an empty queue.
        node = self._min_node
        assert node is not None
        # AVL-specific O(1) successor; this shortcut is not valid for any BST.
        self._min_node = node.right if node.right is not None else node.parent
        self._remove_extreme(node, node.right)
        return minimum

    def remove_max(self) -> int:
        """Remove and return the largest key in O(log n) time."""
        maximum = self.find_max()
        node = self._max_node
        assert node is not None
        self._max_node = node.left if node.left is not None else node.parent
        self._remove_extreme(node, node.left)
        return maximum

    def _remove_extreme(
        self, node: _AVLNode, child: Optional[_AVLNode]
    ) -> None:
        """Splice out an extreme (at most one child), then repair ancestors."""
        parent = node.parent
        self._replace_node(node, child)
        self._size -= 1
        if self._size == 0:
            self._min_node = self._max_node = None
        # Detach the removed node; surviving nodes keep their identities/keys.
        node.left = node.right = node.parent = None
        self._rebalance_upwards(parent)

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

    def _replace_node(
        self, node: _AVLNode, replacement: Optional[_AVLNode]
    ) -> None:
        """Reconnect a subtree to its parent (or update the root)."""
        parent = node.parent
        if parent is None:
            self._root = replacement
        elif parent.left is node:
            parent.left = replacement
        else:
            assert parent.right is node
            parent.right = replacement
        if replacement is not None:
            replacement.parent = parent

    def _rebalance_upwards(self, node: Optional[_AVLNode]) -> None:
        """Repair all ancestors using parent links, with no recursion stack."""
        while node is not None:
            subtree_root = self._rebalance(node)
            node = subtree_root.parent

    @staticmethod
    def _height(node: Optional[_AVLNode]) -> int:
        return node.height if node is not None else 0

    def _rebalance(self, node: _AVLNode) -> _AVLNode:
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._height(node.left) - self._height(node.right)

        if balance > 1:
            assert node.left is not None
            if self._height(node.left.left) < self._height(node.left.right):
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            assert node.right is not None
            if self._height(node.right.right) < self._height(node.right.left):
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _rotate_left(self, node: _AVLNode) -> _AVLNode:
        pivot = node.right
        assert pivot is not None
        self._replace_node(node, pivot)
        node.right = pivot.left
        if node.right is not None:
            node.right.parent = node
        pivot.left = node
        node.parent = pivot
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        pivot.height = 1 + max(self._height(pivot.left), self._height(pivot.right))
        return pivot

    def _rotate_right(self, node: _AVLNode) -> _AVLNode:
        pivot = node.left
        assert pivot is not None
        self._replace_node(node, pivot)
        node.left = pivot.right
        if node.left is not None:
            node.left.parent = node
        pivot.right = node
        node.parent = pivot
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        pivot.height = 1 + max(self._height(pivot.left), self._height(pivot.right))
        return pivot



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
