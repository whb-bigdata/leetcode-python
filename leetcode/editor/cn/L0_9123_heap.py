"""基于数组实现的最小堆。"""

from __future__ import annotations

from typing import Generic, Iterable, List, TypeVar


T = TypeVar("T")


class MinHeap(Generic[T]):
    """满足父节点不大于子节点的二叉最小堆。"""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._items: List[T] = list(values)
        self._heapify()

    def push(self, value: T) -> None:
        """插入元素，并通过上浮恢复最小堆性质，时间复杂度 O(log n)。"""
        self._items.append(value)
        self._sift_up(len(self._items) - 1)

    def pop(self) -> T:
        """移除并返回最小元素，时间复杂度 O(log n)。"""
        if self.is_empty():
            raise IndexError("pop from an empty heap")

        minimum = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last
            self._sift_down(0)
        return minimum

    def peek(self) -> T:
        """查看最小元素但不移除它，时间复杂度 O(1)。"""
        if self.is_empty():
            raise IndexError("peek from an empty heap")
        return self._items[0]

    def size(self) -> int:
        """返回堆中的元素数量，时间复杂度 O(1)。"""
        return len(self._items)

    def is_empty(self) -> bool:
        """返回堆是否为空，时间复杂度 O(1)。"""
        return not self._items

    def to_list(self) -> List[T]:
        """返回底层数组快照；该顺序不是完整排序结果。"""
        return list(self._items)

    def _heapify(self) -> None:
        """自底向上建堆，时间复杂度 O(n)。"""
        for index in range((len(self._items) - 2) // 2, -1, -1):
            self._sift_down(index)

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self._items[parent] <= self._items[index]:
                return
            self._items[parent], self._items[index] = (
                self._items[index],
                self._items[parent],
            )
            index = parent

    def _sift_down(self, index: int) -> None:
        size = len(self._items)
        while True:
            left = index * 2 + 1
            right = left + 1
            smallest = index

            if left < size and self._items[left] < self._items[smallest]:
                smallest = left
            if right < size and self._items[right] < self._items[smallest]:
                smallest = right
            if smallest == index:
                return

            self._items[index], self._items[smallest] = (
                self._items[smallest],
                self._items[index],
            )
            index = smallest


if __name__ == "__main__":
    heap = MinHeap([7, 3, 9, 1, 5])
    print("Heap array:", heap.to_list())
    heap.push(2)
    print("Minimum:", heap.peek())
    print("Sorted removals:", [heap.pop() for _ in range(heap.size())])
