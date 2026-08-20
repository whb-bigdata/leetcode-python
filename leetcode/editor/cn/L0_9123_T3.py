from typing import Any

from IPython.external.qt_loaders import QT_API_PYQT6

from L0_9123_node import Node
#Q3
class LinkedStack:
    def __init__(self):
        self._head = None
        self._size = 0

    def push(self,data:str) -> None:
        new_node = Node(data)
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def pop(self) -> Any | None:
        if self.is_empty():
            raise Exception("Stack is empty!")

        popped_data = self._head.data
        self._head = self._head.next
        self._size -= 1
        return popped_data

    def is_empty(self) -> bool:
        return self._head is None

    def top(self) -> str:
        if self.is_empty():
            raise Exception("Stack is empty!")
        return self._head.data


def print_singly_list(head: Node) -> None:
    """打印单链表"""
    curr = head
    elements = []
    while curr:
        elements.append(str(curr.data))
        curr = curr.next
    print("singly_list: " + (" -> ".join(elements) if elements else "empty"))

#Q4
class LinkedQueue:

    def __init__(self):
        self._head: Node = None  # 指向队头（Front），负责 dequeue (出队)
        self._tail: Node = None  # 指向队尾（Rear），负责 enqueue (入队)
        self._size: int = 0  # 永久计步器

    def is_empty(self) -> bool:
        return self._head is None

    def size(self) -> int:
        return self._size

    def first(self) -> int:
        if self.is_empty():
            raise Exception("Queue is empty!")
        return self._head.data

    def enqueue(self, data: int) -> None:
        new_node = Node(data)

        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1

    def dequeue(self) -> int:
        """出队：从队头拿走并离开 (O(1) 复杂度)"""
        if self.is_empty():
            raise Exception("Queue is empty!")

        popped_data = self._head.data

        self._head = self._head.next
        self._size -= 1

        if self._head is None:
            self._tail = None

        return popped_data

#Q5   O1


#Q6

class ExtendedQueue:


    def __init__(self):
        self._head: Node = None
        self._tail: Node = None

        self._size: int = 0
        self._sum: float = 0.0

    def is_empty(self) -> bool:
        return self._head is None

    def size(self) -> int:
        return self._size

    def first(self) -> int:
        if self.is_empty():
            raise Exception("Queue is empty!")
        return self._head.data

    def enqueue(self, data: int) -> None:

        new_node = Node(data)

        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

        self._sum += data
        self._size += 1

    def dequeue(self) -> int:

        if self.is_empty():
            raise Exception("Queue is empty!")

        popped_data = self._head.data

        self._head = self._head.next
        if self._head is None:
            self._tail = None

        self._sum -= popped_data
        self._size -= 1

        return popped_data

    def get_average(self) -> float:
        """
        核心操作：在 O(1) 时间内计算并返回平均值
        时间复杂度: O(1)
        """
        if self.is_empty():
            raise Exception("Queue is empty! Cannot compute average of 0 elements.")

        return self._sum / self._size

#Q8
class Stack:
    """标准 LIFO 栈"""

    def __init__(self):
        self._data = []

    def push(self, e):
        self._data.append(e)

    def pop(self):
        if self.is_empty():
            raise Exception("Stack is empty")
        return self._data.pop()

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


class TwoStackQueue:
    """使用两个栈模拟的 FIFO 队列"""

    def __init__(self):
        self.in_stack = Stack()  # 负责处理入队
        self.out_stack = Stack()  # 负责处理出队

    def is_empty(self) -> bool:
        return self.in_stack.is_empty() and self.out_stack.is_empty()

    def size(self) -> int:
        return self.in_stack.size() + self.out_stack.size()

    def enqueue(self, e: int) -> None:
        """入队操作"""
        self.in_stack.push(e)

    def dequeue(self) -> int:
        """出队操作"""
        if self.is_empty():
            raise Exception("Queue is empty!")

        # 如果 out_stack 为空，将 in_stack 中的元素全部倒进 out_stack
        if self.out_stack.is_empty():
            while not self.in_stack.is_empty():
                self.out_stack.push(self.in_stack.pop())

        return self.out_stack.pop()

    def first(self) -> int:
        """查看队头元素"""
        if self.is_empty():
            raise Exception("Queue is empty!")

        if self.out_stack.is_empty():
            while not self.in_stack.is_empty():
                self.out_stack.push(self.in_stack.pop())

        # 临时弹出，记录后压回
        temp = self.out_stack.pop()
        self.out_stack.push(temp)
        return temp

#create node

name_pool = ["Alice", "Bob", "Charlie", "David", "Emma", "Fiona", "George",
             "Hannah", "Ian", "Jack", "Kevin", "Lily", "Mason", "Nora"]

singly_names = name_pool

# 构建单链表
singly_head = None
singly_tail = None
for name in singly_names:
    new_node = Node(name)
    if  singly_head is None:
        singly_head = new_node
        singly_tail = new_node
    else:
        singly_tail.next = new_node
        singly_tail = new_node

# Q9
class Node:
    def __init__(self, data: int, next_node=None):
        self.data = data
        self.next = next_node


def reverse_list(head: Node) -> Node:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def is_palindrome(head: Node) -> bool:
    if not head or not head.next:
        return True

    slow = head
    fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    second_half_start = reverse_list(slow.next)

    p1 = head
    p2 = second_half_start
    palindrome = True
    while p2:
        if p1.data != p2.data:
            palindrome = False
            break
        p1 = p1.next
        p2 = p2.next

    slow.next = reverse_list(second_half_start)

    return palindrome



if __name__ == '__main__':
    #use stack
    browser_history = LinkedStack()
    browser_history.push("Alice")
    browser_history.push("Bob")
    print(browser_history.pop())
    print(browser_history.pop())

    #use queue
    use_queue = LinkedQueue()
    use_queue.enqueue("Alice")
    use_queue.enqueue("Bob")
    print(use_queue.dequeue())
    print(use_queue.dequeue())
