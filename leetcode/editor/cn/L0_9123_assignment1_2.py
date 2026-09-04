"""Undoable queue with a last-k operation history.

The current queue is a doubly linked list. Undo and redo share one fixed-size
circular array. Each history slot stores the operation, its value, and two
array indices linking the records in the current branch.

All four public operations take O(1) worst-case time. The queue uses O(n)
space and the history uses O(k) additional space.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, List, Optional, TypeVar


T = TypeVar("T")


@dataclass
class _QueueNode(Generic[T]):
    value: T
    prev: Optional["_QueueNode[T]"] = None
    next: Optional["_QueueNode[T]"] = None


class _DoublyLinkedQueue(Generic[T]):
    """A deque implemented explicitly as a doubly linked list."""

    def __init__(self) -> None:
        self.front: Optional[_QueueNode[T]] = None
        self.back: Optional[_QueueNode[T]] = None
        self.length = 0

    def add_first(self, value: T) -> None:
        node = _QueueNode(value=value, next=self.front)
        if self.front is None:
            self.back = node
        else:
            self.front.prev = node
        self.front = node
        self.length += 1

    def add_last(self, value: T) -> None:
        node = _QueueNode(value=value, prev=self.back)
        if self.back is None:
            self.front = node
        else:
            self.back.next = node
        self.back = node
        self.length += 1

    def remove_first(self) -> T:
        if self.front is None:
            raise IndexError("remove from an empty queue")
        node = self.front
        self.front = node.next
        if self.front is None:
            self.back = None
        else:
            self.front.prev = None
        self.length -= 1
        return node.value

    def remove_last(self) -> T:
        if self.back is None:
            raise IndexError("remove from an empty queue")
        node = self.back
        self.back = node.prev
        if self.back is None:
            self.front = None
        else:
            self.back.next = None
        self.length -= 1
        return node.value

    def __iter__(self) -> Iterator[T]:
        node = self.front
        while node is not None:
            yield node.value
            node = node.next


@dataclass
class _HistoryRecord(Generic[T]):
    """A history item; prev and next are circular-array indices."""

    kind: str
    value: T
    prev: Optional[int]
    next: Optional[int]


class RollbackQueue(Generic[T]):
    """FIFO queue with O(1) worst-case enqueue, dequeue, undo, and redo."""

    ENQUEUE = "ENQUEUE"
    DEQUEUE = "DEQUEUE"

    def __init__(self, k: int) -> None:
        if k < 0:
            raise ValueError("k must be non-negative")

        self._queue: _DoublyLinkedQueue[T] = _DoublyLinkedQueue()
        self._capacity = k
        self._history: List[Optional[_HistoryRecord[T]]] = [None] * k

        # Indices of the current history branch.
        self._first: Optional[int] = None
        self._last: Optional[int] = None
        self._cursor: Optional[int] = None

        # Only enqueue/dequeue advances next_slot; undo/redo never changes age.
        self._next_slot = 0
        self._filled = 0

    def enqueue(self, value: T) -> None:
        self._queue.add_last(value)
        self._record(self.ENQUEUE, value)

    def dequeue(self) -> T:
        value = self._queue.remove_first()
        self._record(self.DEQUEUE, value)
        return value

    def undo(self) -> bool:
        if self._cursor is None:
            return False

        record = self._record_at(self._cursor)
        if record.kind == self.ENQUEUE:
            removed = self._queue.remove_last()
            assert removed == record.value
        else:
            self._queue.add_first(record.value)

        self._cursor = record.prev
        return True

    def redo(self) -> bool:
        if self._first is None:
            return False

        if self._cursor is None:
            index = self._first
        else:
            index = self._record_at(self._cursor).next

        if index is None:
            return False

        record = self._record_at(index)
        if record.kind == self.ENQUEUE:
            self._queue.add_last(record.value)
        else:
            removed = self._queue.remove_first()
            assert removed == record.value

        self._cursor = index
        return True

    def _record(self, kind: str, value: T) -> None:
        """Create one operation slot and discard any redo branch in O(1)."""
        if self._capacity == 0:
            return

        # Keep the applied prefix and detach the entire redo suffix in O(1).
        if self._cursor is None:
            self._first = None
            self._last = None
        else:
            self._record_at(self._cursor).next = None
            self._last = self._cursor

        index = self._next_slot

        # At full capacity, next_slot is the oldest chronological slot. If it
        # remains in this branch, it must be first and is detached in O(1).
        if self._filled == self._capacity:
            if self._first == index:
                old_first = self._record_at(index)
                self._first = old_first.next
                if self._first is None:
                    self._last = None
                    self._cursor = None
                else:
                    self._record_at(self._first).prev = None
        else:
            self._filled += 1

        self._history[index] = _HistoryRecord(
            kind=kind, value=value, prev=self._last, next=None
        )

        if self._last is None:
            self._first = index
        else:
            self._record_at(self._last).next = index

        self._last = index
        self._cursor = index
        self._next_slot = (index + 1) % self._capacity

    def _record_at(self, index: int) -> _HistoryRecord[T]:
        record = self._history[index]
        assert record is not None
        return record

    def front(self) -> T:
        if self._queue.front is None:
            raise IndexError("front from an empty queue")
        return self._queue.front.value

    def size(self) -> int:
        return self._queue.length

    def is_empty(self) -> bool:
        return self._queue.length == 0

    def to_list(self) -> List[T]:
        return list(self._queue)


def _run_checks() -> None:
    # k=3: eviction, repeated undo/redo, and a new branch after undo.
    queue = RollbackQueue[str](3)
    queue.enqueue("A")
    queue.enqueue("B")
    assert queue.dequeue() == "A"
    assert queue.to_list() == ["B"]

    assert queue.undo() and queue.to_list() == ["A", "B"]
    assert queue.undo() and queue.to_list() == ["A"]
    assert queue.redo() and queue.to_list() == ["A", "B"]

    queue.enqueue("C")  # Discards redo(DEQUEUE A); ENQUEUE(A) also expires.
    assert queue.to_list() == ["A", "B", "C"]
    assert queue.undo() and queue.to_list() == ["A", "B"]
    assert queue.undo() and queue.to_list() == ["A"]
    assert not queue.undo()
    assert queue.redo() and queue.to_list() == ["A", "B"]
    assert queue.redo() and queue.to_list() == ["A", "B", "C"]
    assert not queue.redo()

    # Mixed operations after the history window is full.
    mixed = RollbackQueue[int](2)
    mixed.enqueue(1)
    mixed.enqueue(2)
    assert mixed.dequeue() == 1
    assert mixed.undo() and mixed.to_list() == [1, 2]
    assert mixed.undo() and mixed.to_list() == [1]
    assert not mixed.undo()
    assert mixed.redo() and mixed.to_list() == [1, 2]
    assert mixed.redo() and mixed.to_list() == [2]

    # k=0 keeps no history but normal queue operations still work.
    no_history = RollbackQueue[int](0)
    no_history.enqueue(7)
    assert no_history.dequeue() == 7
    assert not no_history.undo()
    assert not no_history.redo()

    print("RollbackQueue checks passed")


if __name__ == "__main__":
    _run_checks()
