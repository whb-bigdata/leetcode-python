"""基于最小堆实现的稳定优先队列。"""

from __future__ import annotations

from typing import Generic, TypeVar

from L0_9123_heap import MinHeap


T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """数值越小，优先级越高；相同优先级按入队顺序出队。"""

    def __init__(self) -> None:
        # 元组格式为 (priority, insertion_order, value)。
        # insertion_order 保证相同优先级时不会比较 value，且保持稳定顺序。
        self._heap: MinHeap[tuple[int, int, T]] = MinHeap()
        self._next_order = 0

    def enqueue(self, value: T, priority: int) -> None:
        """加入元素，时间复杂度 O(log n)。"""
        self._heap.push((priority, self._next_order, value))
        self._next_order += 1

    def dequeue(self) -> T:
        """移除并返回优先级最高的元素，时间复杂度 O(log n)。"""
        return self._heap.pop()[2]

    def peek(self) -> T:
        """查看优先级最高的元素但不移除它，时间复杂度 O(1)。"""
        return self._heap.peek()[2]

    def size(self) -> int:
        """返回队列元素数量，时间复杂度 O(1)。"""
        return self._heap.size()

    def is_empty(self) -> bool:
        """返回队列是否为空，时间复杂度 O(1)。"""
        return self._heap.is_empty()


if __name__ == "__main__":
    queue = PriorityQueue[str]()
    queue.enqueue("normal task", priority=3)
    queue.enqueue("urgent task", priority=1)
    queue.enqueue("another urgent task", priority=1)
    queue.enqueue("low-priority task", priority=5)

    print("Next task:", queue.peek())
    while not queue.is_empty():
        print("Dequeued:", queue.dequeue())
