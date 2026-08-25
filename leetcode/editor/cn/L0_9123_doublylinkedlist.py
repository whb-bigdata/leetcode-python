"""A generic doubly linked list implementation."""

from __future__ import annotations

from typing import Generic, Optional, TypeVar

from Node import Node


T = TypeVar("T")


class DoublyLinkedList(Generic[T]):
    """A doubly linked list whose end nodes have a ``None`` outer link."""

    def __init__(self, front: Optional[Node[T]] = None) -> None:
        """Initialise the list with an optional first node."""
        self._size = 1 if front is not None else 0
        self._front = front
        self._back = front
        if front is not None:
            front.set_prev(None)
            front.set_next(None)

    def first(self) -> Optional[Node[T]]:
        """Return the first node in the list, or ``None`` when empty."""
        return self._front

    def last(self) -> Optional[Node[T]]:
        """Return the last node in the list, or ``None`` when empty."""
        return self._back

    def before(self, p: Optional[Node[T]]) -> Optional[Node[T]]:
        """Return the node immediately before ``p``."""
        return p.get_prev() if self._contains(p) else None

    def after(self, p: Optional[Node[T]]) -> Optional[Node[T]]:
        """Return the node immediately after ``p``."""
        return p.get_next() if self._contains(p) else None

    def insert_before(self, p: Optional[Node[T]], e: Node[T]) -> None:
        """Insert ``e`` immediately before ``p``.

        When the list is empty, ``p`` must be ``None`` and ``e`` becomes the
        first node. An invalid position leaves the list unchanged.
        """
        if self.is_empty():
            if p is None:
                self._insert_into_empty_list(e)
            return
        if not self._contains(p):
            return

        previous = p.get_prev()
        e.set_prev(previous)
        e.set_next(p)
        p.set_prev(e)
        if previous is None:
            self._front = e
        else:
            previous.set_next(e)
        self._size += 1

    def insert_after(self, p: Optional[Node[T]], e: Node[T]) -> None:
        """Insert ``e`` immediately after ``p``.

        When the list is empty, ``p`` must be ``None`` and ``e`` becomes the
        first node. An invalid position leaves the list unchanged.
        """
        if self.is_empty():
            if p is None:
                self._insert_into_empty_list(e)
            return
        if not self._contains(p):
            return

        following = p.get_next()
        e.set_prev(p)
        e.set_next(following)
        p.set_next(e)
        if following is None:
            self._back = e
        else:
            following.set_prev(e)
        self._size += 1

    def remove(self, p: Optional[Node[T]]) -> Optional[Node[T]]:
        """Remove and return ``p``; return ``None`` for an invalid node."""
        if not self._contains(p):
            return None

        previous = p.get_prev()
        following = p.get_next()
        if previous is None:
            self._front = following
        else:
            previous.set_next(following)
        if following is None:
            self._back = previous
        else:
            following.set_prev(previous)

        p.set_prev(None)
        p.set_next(None)
        self._size -= 1
        return p

    def size(self) -> int:
        """Return the number of nodes in the list."""
        return self._size

    def is_empty(self) -> bool:
        """Return ``True`` if the list has no nodes."""
        return self._size == 0

    def _insert_into_empty_list(self, e: Node[T]) -> None:
        """Make ``e`` the sole node in an empty list."""
        e.set_prev(None)
        e.set_next(None)
        self._front = e
        self._back = e
        self._size = 1

    def _contains(self, node: Optional[Node[T]]) -> bool:
        """Return whether ``node`` is one of this list's nodes."""
        current = self._front
        while current is not None:
            if current is node:
                return True
            current = current.get_next()
        return False
