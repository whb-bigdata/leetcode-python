"""一个支持撤销（undo）和重做（redo）的固定历史队列。

队列的当前内容占用 O(n) 空间；n 是队列中的元素数量。回滚功能使用
固定大小为 k 的环形历史缓冲区，因此额外空间始终为 O(k)。
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Generic, List, Optional, Tuple, TypeVar


T = TypeVar("T")
Operation = Tuple[str, T]


class RollbackQueue(Generic[T]):
    """支持入队、出队、撤销和重做的 FIFO 队列。

    ``history_limit`` 是可撤销操作的最大数量 k。历史满时，最旧的一次
    操作会被遗忘，因而不能再撤销；这保证了历史记录不会无限增长。
    """

    def __init__(self, history_limit: int) -> None:
        if history_limit < 0:
            raise ValueError("history_limit must be non-negative")

        self._items: Deque[T] = deque()
        self._history_limit = history_limit

        # 环形数组保存从最旧到最新的历史操作。每条记录只需操作类型和值。
        self._history: List[Optional[Operation]] = [None] * history_limit
        self._history_start = 0
        self._history_size = 0

        # cursor 左侧的记录已经应用到队列，右侧的记录可以 redo。
        # 不变量：0 <= _cursor <= _history_size <= history_limit。
        self._cursor = 0

    def enqueue(self, value: T) -> None:
        """将 ``value`` 放入队尾，时间复杂度为 O(1)。"""
        self._items.append(value)
        self._record_operation(("enqueue", value))

    def dequeue(self) -> T:
        """移除并返回队首元素；空队列时抛出 ``IndexError``，时间为 O(1)。"""
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")

        value = self._items.popleft()
        self._record_operation(("dequeue", value))
        return value

    def undo(self) -> bool:
        """撤销最近一次可撤销操作；没有可撤销操作时返回 ``False``。

        正确性：历史记录按操作发生顺序保存。撤销最近的入队时，它仍是
        队尾，故 ``pop`` 恰好移除该元素；撤销最近的出队时，使用
        ``appendleft`` 恢复原来的队首。两种逆操作都会恢复操作前的状态。
        """
        if self._cursor == 0:
            return False

        operation = self._operation_at(self._cursor - 1)
        kind, value = operation
        if kind == "enqueue":
            self._items.pop()
        else:  # kind == "dequeue"
            self._items.appendleft(value)
        self._cursor -= 1
        return True

    def redo(self) -> bool:
        """重做最近一次被撤销的操作；没有可重做操作时返回 ``False``。

        正确性：cursor 右侧的第一条历史正是下一次被撤销的操作。按原始
        方向再次执行该操作，就会回到撤销前的状态。
        """
        if self._cursor == self._history_size:
            return False

        operation = self._operation_at(self._cursor)
        kind, value = operation
        if kind == "enqueue":
            self._items.append(value)
        else:  # kind == "dequeue"
            self._items.popleft()
        self._cursor += 1
        return True

    def front(self) -> T:
        """返回队首但不移除它，时间复杂度为 O(1)。"""
        if self.is_empty():
            raise IndexError("front from an empty queue")
        return self._items[0]

    def size(self) -> int:
        """返回当前队列元素数，时间复杂度为 O(1)。"""
        return len(self._items)

    def is_empty(self) -> bool:
        """判断队列是否为空，时间复杂度为 O(1)。"""
        return not self._items

    def to_list(self) -> List[T]:
        """以队首到队尾的顺序返回快照，时间和空间复杂度为 O(n)。"""
        return list(self._items)

    def _record_operation(self, operation: Operation) -> None:
        """以 O(1) 时间写入一条新历史记录。

        新操作会使 redo 分支失效。这里仅移动逻辑长度，不逐项清理旧 redo
        记录，避免 ``clear`` 造成 O(k) 的单次开销。随后覆盖一个环形槽位；
        历史满时前移起点以忘记最旧记录。因此本方法最坏仍为 O(1)。
        """
        if self._history_limit == 0:
            return

        # 逻辑删除 redo 分支：cursor 右侧记录不再有效。
        self._history_size = self._cursor
        if self._history_size < self._history_limit:
            index = (self._history_start + self._history_size) % self._history_limit
            self._history[index] = operation
            self._history_size += 1
            self._cursor = self._history_size
            return

        # 缓冲区已满：覆盖最旧记录，再将最旧位置右移一格。
        self._history[self._history_start] = operation
        self._history_start = (self._history_start + 1) % self._history_limit
        self._cursor = self._history_limit

    def _operation_at(self, offset: int) -> Operation:
        """取得逻辑历史中的第 ``offset`` 条记录，时间复杂度为 O(1)。"""
        index = (self._history_start + offset) % self._history_limit
        operation = self._history[index]
        assert operation is not None
        return operation


if __name__ == "__main__":
    queue = RollbackQueue[str](history_limit=3)
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")
    print("Initial queue:", queue.to_list())

    print("Dequeued:", queue.dequeue())
    print("After dequeue:", queue.to_list())

    queue.undo()
    print("After undo:", queue.to_list())
    queue.redo()
    print("After redo:", queue.to_list())
