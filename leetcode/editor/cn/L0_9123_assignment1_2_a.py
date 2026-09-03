"""COMP9123 Assignment 1 - Question 2(a): Undoable Queue.

The queue itself is a doubly linked list.  A fixed-size circular array stores
the last k issued enqueue/dequeue operations.  Undo and redo do not change the
monotonic issued_count, so an operation keeps its original age in the history
window even while it is undone.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, Iterator, Optional, TypeVar


T = TypeVar("T")


class OperationType(Enum):
    ENQUEUE = auto()
    DEQUEUE = auto()


class RecordState(Enum):
    NONE = auto()
    UNDO = auto()
    REDO = auto()


@dataclass
class Node(Generic[T]):
    value: T
    prev: Optional["Node[T]"] = None
    next: Optional["Node[T]"] = None
    in_queue: bool = False


@dataclass
class HistoryRecord(Generic[T]):
    operation_type: OperationType
    node: Node[T]
    state: RecordState = RecordState.NONE
    prev_index: Optional[int] = None
    next_index: Optional[int] = None
    epoch: int = -1


class UndoableQueue(Generic[T]):
    """A queue with O(1) worst-case enqueue, dequeue, undo, and redo."""

    def __init__(self, k: int) -> None:
        if k <= 0:
            raise ValueError("k must be a positive integer")

        self.capacity = k
        self.front: Optional[Node[T]] = None
        self.back: Optional[Node[T]] = None

        # Slots are initialised lazily.  A slot is read only after it has been
        # written, or when issued_count >= capacity and it must be evicted.
        self.history: list[Optional[HistoryRecord[T]]] = [None] * k
        self.issued_count = 0

        # U and R are intrusive doubly linked stacks whose links are stored in
        # the HistoryRecord objects.  Only their top indices are required.
        self.undo_top: Optional[int] = None
        self.redo_top: Optional[int] = None
        self.redo_epoch = 0

    def __len__(self) -> int:
        size = 0
        node = self.front
        while node is not None:
            size += 1
            node = node.next
        return size

    def __iter__(self) -> Iterator[T]:
        node = self.front
        while node is not None:
            yield node.value
            node = node.next

    def to_list(self) -> list[T]:
        return list(self)

    def _append_node(self, node: Node[T]) -> None:
        if node.in_queue:
            raise RuntimeError("node is already in the queue")
        node.prev = self.back
        node.next = None
        if self.back is None:
            self.front = node
        else:
            self.back.next = node
        self.back = node
        node.in_queue = True

    def _prepend_node(self, node: Node[T]) -> None:
        if node.in_queue:
            raise RuntimeError("node is already in the queue")
        node.prev = None
        node.next = self.front
        if self.front is None:
            self.back = node
        else:
            self.front.prev = node
        self.front = node
        node.in_queue = True

    def _remove_front_node(self) -> Node[T]:
        node = self.front
        if node is None:
            raise IndexError("dequeue from an empty queue")
        self.front = node.next
        if self.front is None:
            self.back = None
        else:
            self.front.prev = None
        node.prev = None
        node.next = None
        node.in_queue = False
        return node

    def _remove_back_node(self) -> Node[T]:
        node = self.back
        if node is None:
            raise RuntimeError("history and queue state are inconsistent")
        self.back = node.prev
        if self.back is None:
            self.front = None
        else:
            self.back.next = None
        node.prev = None
        node.next = None
        node.in_queue = False
        return node

    def _record_at(self, index: int) -> HistoryRecord[T]:
        record = self.history[index]
        if record is None:
            raise RuntimeError("history slot is unexpectedly empty")
        return record

    def _clear_redo(self) -> None:
        # Old redo records become stale without an O(k) scan.
        self.redo_epoch += 1
        self.redo_top = None

    def _unlink_undo(self, index: int) -> None:
        record = self._record_at(index)
        if record.prev_index is not None:
            self._record_at(record.prev_index).next_index = record.next_index
        if record.next_index is not None:
            self._record_at(record.next_index).prev_index = record.prev_index
        else:
            self.undo_top = record.prev_index
        record.state = RecordState.NONE
        record.prev_index = None
        record.next_index = None

    def _unlink_redo(self, index: int) -> None:
        record = self._record_at(index)
        if record.prev_index is not None:
            self._record_at(record.prev_index).next_index = record.next_index
        if record.next_index is not None:
            self._record_at(record.next_index).prev_index = record.prev_index
        else:
            self.redo_top = record.prev_index
        record.state = RecordState.NONE
        record.prev_index = None
        record.next_index = None

    def _push_undo(self, index: int) -> None:
        record = self._record_at(index)
        record.prev_index = self.undo_top
        record.next_index = None
        if self.undo_top is not None:
            self._record_at(self.undo_top).next_index = index
        self.undo_top = index
        record.state = RecordState.UNDO

    def _push_redo(self, index: int) -> None:
        record = self._record_at(index)
        record.prev_index = self.redo_top
        record.next_index = None
        if self.redo_top is not None:
            self._record_at(self.redo_top).next_index = index
        self.redo_top = index
        record.state = RecordState.REDO
        record.epoch = self.redo_epoch

    def _evict(self, index: int) -> None:
        record = self._record_at(index)
        if record.state is RecordState.UNDO:
            self._unlink_undo(index)
        elif (
            record.state is RecordState.REDO
            and record.epoch == self.redo_epoch
        ):
            self._unlink_redo(index)

    def _record(self, operation_type: OperationType, node: Node[T]) -> None:
        index = self.issued_count % self.capacity
        if self.issued_count >= self.capacity:
            self._evict(index)

        self.history[index] = HistoryRecord(operation_type, node)
        self._push_undo(index)
        self.issued_count += 1

    def enqueue(self, value: T) -> None:
        self._clear_redo()
        node = Node(value)
        self._append_node(node)
        self._record(OperationType.ENQUEUE, node)

    def dequeue(self) -> T:
        if self.front is None:
            raise IndexError("dequeue from an empty queue")
        self._clear_redo()
        node = self._remove_front_node()
        self._record(OperationType.DEQUEUE, node)
        return node.value

    def undo(self) -> None:
        if self.undo_top is None:
            return

        index = self.undo_top
        record = self._record_at(index)
        self._unlink_undo(index)

        if record.operation_type is OperationType.ENQUEUE:
            removed = self._remove_back_node()
            if removed is not record.node:
                raise RuntimeError("history and queue state are inconsistent")
        else:
            self._prepend_node(record.node)

        self._push_redo(index)

    def redo(self) -> None:
        if self.redo_top is None:
            return

        index = self.redo_top
        record = self._record_at(index)
        self._unlink_redo(index)

        if record.operation_type is OperationType.ENQUEUE:
            self._append_node(record.node)
        else:
            removed = self._remove_front_node()
            if removed is not record.node:
                raise RuntimeError("history and queue state are inconsistent")

        self._push_undo(index)


def _self_test() -> None:
    # Worked example from the assignment.
    queue: UndoableQueue[str] = UndoableQueue(3)
    queue.enqueue("A")
    queue.enqueue("B")
    queue.undo()
    assert queue.to_list() == ["A"]
    queue.redo()
    assert queue.to_list() == ["A", "B"]
    queue.enqueue("C")
    queue.enqueue("D")
    queue.undo()
    assert queue.to_list() == ["A", "B", "C"]

    # A new issued operation discards the redo branch but still advances age.
    queue = UndoableQueue(3)
    queue.enqueue("A")  # op1
    queue.enqueue("B")  # op2
    queue.enqueue("C")  # op3
    queue.undo()
    queue.undo()
    queue.enqueue("D")  # op4; op1 is evicted, op2/op3 cannot be redone
    assert queue.to_list() == ["A", "D"]
    queue.redo()
    assert queue.to_list() == ["A", "D"]
    queue.undo()
    assert queue.to_list() == ["A"]
    queue.undo()  # op1 is outside the last-three issued slots
    assert queue.to_list() == ["A"]

    # Mixed enqueue/dequeue followed by undo and redo.
    queue = UndoableQueue(4)
    queue.enqueue("A")
    queue.enqueue("B")
    assert queue.dequeue() == "A"
    assert queue.to_list() == ["B"]
    queue.undo()
    assert queue.to_list() == ["A", "B"]
    queue.redo()
    assert queue.to_list() == ["B"]
    queue.undo()
    queue.undo()
    assert queue.to_list() == ["A"]


if __name__ == "__main__":
    _self_test()
    print("All UndoableQueue tests passed.")
