import random

from xxlimited_35 import Null


class Node:
    def __init__(self, data: int = 0, next=None):
        self.data = data
        self.next = next

name_pool = ["A", "B", "C", "D"]

singly_names = name_pool
print('')
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
if __name__ == '__main__':
    curr = singly_head
    while curr.next is not None:
        print(curr.data)
        curr=curr.next
    name = 'Fix'
    print(f'output1 {name}')  # method1
    print('output2 {0}'.format(name))  # method2


class DoublyNode:
    def __init__(self, data: int = 0, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


if __name__ == '__main__':
    doubly_values = [random.randint(1, 100) for _ in range(10)]
    doubly_head = None
    doubly_tail = None

    for value in doubly_values:
        new_node = DoublyNode(value, prev=doubly_tail)
        if doubly_head is None:
            doubly_head = new_node
        else:
            doubly_tail.next = new_node
        doubly_tail = new_node

    print('Doubly linked list (forward):')
    curr = doubly_head
    while curr is not None:
        print(curr.data)
        curr = curr.next

    print('Doubly linked list (backward):')
    curr = doubly_tail
    while curr is not None:
        print(curr.data)
        curr = curr.prev
