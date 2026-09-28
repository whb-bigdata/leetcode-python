"""COMP9123 Assignment 2, Question 3: Priority Task Scheduler.

Tasks are stored as (priority, name). A smaller priority value represents a
more urgent task. The heap property compares priorities only.
"""

from __future__ import annotations

from typing import Iterable, List, Tuple


Task = Tuple[int, str]


class MinHeap:
    """An array-based binary min-heap for priority tasks."""

    def __init__(self) -> None:
        """Create an empty task heap."""
        self._heap: List[Task] = []

    def size(self) -> int:
        """Return the number of tasks in O(1) time."""
        return len(self._heap)

    def is_empty(self) -> bool:
        """Return whether the heap has no tasks in O(1) time."""
        return not self._heap

    def peek_min(self) -> Task:
        """Return the most urgent task without removing it, in O(1) time."""
        if self.is_empty():
            raise IndexError("peek_min from an empty heap")
        return self._heap[0]

    def insert(self, priority: int, name: str) -> None:
        """Insert one task and restore the heap property in O(log n) time."""
        self._heap.append((priority, name))
        self._sift_up(self.size() - 1)

    def extract_min(self) -> Task:
        """Remove and return the most urgent task in O(log n) time."""
        if self.is_empty():
            raise IndexError("extract_min from an empty heap")

        minimum = self._heap[0]
        last_task = self._heap.pop()
        if self._heap:
            self._heap[0] = last_task
            self._sift_down(0)
        return minimum

    def parent(self, index: int) -> int:
        """Return the parent index for a non-root node."""
        return (index - 1) // 2

    def left(self, index: int) -> int:
        """Return the left-child index."""
        return 2 * index + 1

    def right(self, index: int) -> int:
        """Return the right-child index."""
        return 2 * index + 2

    def _sift_up(self, index: int) -> None:
        """Move a newly appended task upward until its parent is no larger.

        Each swap moves the task one level closer to the root, so the loop has
        at most the heap height O(log n) iterations.
        """
        while index > 0:
            parent_index = self.parent(index)
            if self._heap[parent_index][0] <= self._heap[index][0]:
                return
            self._heap[parent_index], self._heap[index] = (
                self._heap[index],
                self._heap[parent_index],
            )
            index = parent_index

    def _sift_down(self, index: int) -> None:
        """Move a root replacement downward until the heap property holds.

        Swapping with the smaller child ensures that the parent is no larger
        than either child after each step. The loop takes O(log n) time.
        """
        while True:
            left_index = self.left(index)
            right_index = self.right(index)
            smallest = index

            if (
                left_index < self.size()
                and self._heap[left_index][0] < self._heap[smallest][0]
            ):
                smallest = left_index
            if (
                right_index < self.size()
                and self._heap[right_index][0] < self._heap[smallest][0]
            ):
                smallest = right_index

            if smallest == index:
                return
            self._heap[index], self._heap[smallest] = (
                self._heap[smallest],
                self._heap[index],
            )
            index = smallest

    def build_heap(self, tasks: Iterable[Task]) -> None:
        """Build a valid heap from unordered tasks in O(n) time.

        All leaves already satisfy the heap property. Therefore, process every
        internal node from the last parent back to the root, sifting it down.
        This bottom-up Floyd heap construction is O(n), not O(n log n).
        """
        self._heap = list(tasks)
        last_parent = self.parent(self.size() - 1)
        for index in range(last_parent, -1, -1):
            self._sift_down(index)

    def to_list(self) -> List[Task]:
        """Return a copy of the internal array, useful for testing."""
        return list(self._heap)


if __name__ == "__main__":
    heap = MinHeap()
    for priority, name in [
        (5, "Backup"),
        (1, "SecurityAlert"),
        (3, "EmailDigest"),
        (2, "PatchUpdate"),
    ]:
        heap.insert(priority, name)

    assert heap.peek_min() == (1, "SecurityAlert")
    print("Insert order:", heap.to_list())
    print("Extract order:", [heap.extract_min() for _ in range(heap.size())])

    heap.build_heap([(4, "Report"), (1, "Alert"), (3, "Email"), (2, "Patch")])
    assert [heap.extract_min() for _ in range(heap.size())] == [
        (1, "Alert"),
        (2, "Patch"),
        (3, "Email"),
        (4, "Report"),
    ]
    print("build_heap check passed.")
