"""固定容量循环队列的数组实现。"""

from __future__ import annotations

from typing import Generic, List, Optional, TypeVar, cast


T = TypeVar("T")


class CircularQueue(Generic[T]):
    """使用长度为 ``k`` 的数组实现先进先出队列。"""

    def __init__(self, k: int) -> None:
        """初始化容量为 ``k`` 的空循环队列。"""
        if k <= 0:
            raise ValueError("k must be a positive integer")

        self._capacity = k
        self._items: List[Optional[T]] = [None] * k
        self._front = 0
        # _rear 始终指向下一次入队要写入的位置。
        self._rear = 0
        self._size = 0

    def enqueue(self, value: T) -> bool:
        """将元素加入队尾；队列已满时返回 ``False``，否则返回 ``True``。"""
        if self.is_full():
            return False

        self._items[self._rear] = value
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1
        return True

    def dequeue(self) -> T:
        """移除并返回队首元素；空队列时抛出 ``IndexError``。"""
        if self.is_empty():
            raise IndexError("dequeue from an empty circular queue")

        value = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        # 已入队的位置总是一个 T；cast 也允许 T 本身是 Optional 类型。
        return cast(T, value)

    def front(self) -> T:
        """返回队首元素但不移除它。"""
        if self.is_empty():
            raise IndexError("front from an empty circular queue")
        value = self._items[self._front]
        return cast(T, value)

    def is_empty(self) -> bool:
        """判断队列是否为空。"""
        return self._size == 0

    def is_full(self) -> bool:
        """判断队列是否已达到容量上限。"""
        return self._size == self._capacity

    def size(self) -> int:
        """返回当前队列中的元素数量。"""
        return self._size

    def to_list(self) -> List[T]:
        """按队首到队尾的顺序返回队列快照，用于展示和调试。"""
        values: List[T] = []
        for offset in range(self._size):
            index = (self._front + offset) % self._capacity
            values.append(cast(T, self._items[index]))
        return values


if __name__ == "__main__":
    # 1. 初始化：容量为 3，数组位置为 0、1、2。
    queue = CircularQueue[str](3)
    print("Initial:", queue.to_list())

    # 2. 连续入队，队列达到容量上限。
    for item in ("A", "B", "C"):
        print(f"Enqueue {item}:", queue.enqueue(item), queue.to_list())
    print("Enqueue D when full:", queue.enqueue("D"))

    # 3. 出队两个元素，front 向前移动。
    print("Dequeue:", queue.dequeue(), queue.to_list())
    print("Dequeue:", queue.dequeue(), queue.to_list())

    # 4. 再次入队：rear 使用取模回到数组开头，展示循环效果。
    for item in ("D", "E"):
        print(f"Enqueue {item}:", queue.enqueue(item), queue.to_list())
    print("Final front:", queue.front())
