"""
Singly Linked List Node
-----------------------

This node represents an item in a doubly linked list. Each node stores a
value and links to its next and previous nodes.
"""

from __future__ import annotations

from typing import Generic, Optional, TypeVar


T = TypeVar("T")


class Node(Generic[T]):
    """A node that can be linked in both directions."""

    def __init__(
        self,
        value: T,
        next: Optional[Node[T]] = None,
        prev: Optional[Node[T]] = None,
    ) -> None:
        """Initialise the node with its value and optional neighbours."""
        self._value = value
        self._next = next
        self._prev = prev

    def get_value(self) -> T:
        """Return the value stored by this node."""
        return self._value

    def set_value(self, value: T) -> None:
        """Set the value stored by this node."""
        self._value = value

    def get_next(self) -> Optional[Node[T]]:
        """Return the node immediately after this node, if any."""
        return self._next

    def set_next(self, next: Optional[Node[T]]) -> None:
        """Set the node immediately after this node."""
        self._next = next

    def get_prev(self) -> Optional[Node[T]]:
        """Return the node immediately before this node, if any."""
        return self._prev

    def set_prev(self, prev: Optional[Node[T]]) -> None:
        """Set the node immediately before this node."""
        self._prev = prev
