# Q1
class Node:
    def __init__(self, data: int = 0, next=None):
        self.data = data
        self.next = next

class DoublyNode:
    """双链表节点[cite: 1]"""
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

def print_singly_list(head: Node) -> None:
    """打印单链表"""
    curr = head
    elements = []
    while curr:
        elements.append(str(curr.data))
        curr = curr.next
    print("singly_list: " + (" -> ".join(elements) if elements else "empty"))

def print_doubly_list(head: DoublyNode) -> None:
    """打印双链表（正向与反向校验）"""
    curr = head
    elements = []
    while curr:
        elements.append(str(curr.data))
        curr = curr.next
    print("doubly_list: " + (" <-> ".join(elements) if elements else "empty"))


name_pool = ["Alice", "Bob", "Charlie", "David", "Emma", "Fiona", "George",
             "Hannah", "Ian", "Jack", "Kevin", "Lily", "Mason", "Nora"]

# 随机抽取 10 个不重复的名字
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

doubly_names = name_pool
# 构建双链表
doubly_head = None
doubly_tail = None
for name in doubly_names:
    new_node = DoublyNode(name)
    if not doubly_head:
        doubly_head = new_node
        doubly_tail = new_node
    else:
        new_node.prev = doubly_tail
        doubly_tail.next = new_node
        doubly_tail = new_node

# Q2
def traverse(head: Node) -> None:
    current = head
    elements = []
    while current:
        elements.append(str(current.data))
        current = current.next
    print(" -> ".join(elements) if elements else "Empty List")

# Q3
class DoublyNode:
    def __init__(self, data: int = 0, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

# Q4
def insert_at_beginning(head: Node, new_data: int) -> Node:
    new_node = Node(new_data)
    new_node.next = head
    return new_node  # 返回新的头节点

# Q5

def delete_node_by_value(head: Node, key: str) -> Node:
    """
    根据给定值删除单链表中的节点[cite: 1]
    包含边界情况处理：
    1. 链表为空
    2. 删除头节点
    3. 删除中间或尾部节点
    4. 目标节点不存在
    """
    # 边界情况 1：空链表[cite: 1]
    if not head:
        print(f"删除失败：链表为空。")
        return None

    # 边界情况 2：要删除的是头节点[cite: 1]
    if head.data == key:
        print(f"成功删除头节点: {key}")
        return head.next

    # 处理删除中间节点或尾节点[cite: 1]
    curr = head
    while curr.next and curr.next.data != key:
        curr = curr.next

    # 边界情况 3：未找到匹配的节点[cite: 1]
    if not curr.next:
        print(f"未找到值为 '{key}' 的节点，链表保持不变。")
        return head

    # 找到节点并删除
    print(f"成功删除节点: {key}")
    curr.next = curr.next.next
    return head

# Q6
def delete_node(head: DoublyNode, key: int) -> DoublyNode:
    current = head

    # 查找值为 key 的节点
    while current and current.data != key:
        current = current.next

    # 如果未找到该节点
    if not current:
        return head

    # 如果要删除的是头节点
    if current == head:
        head = current.next
        if head:
            head.prev = None
        return head

    # 如果要删除的是中间或尾部节点
    if current.prev:
        current.prev.next = current.next
    if current.next:
        current.next.prev = current.prev

    return head
# Q7_1

def traverse_reverse_o1(head: Node) -> None:
    # 1. 计算链表总长度
    n = 0
    curr = head
    while curr:
        n += 1
        curr = curr.next

    # 2. 从后向前按索引访问
    for i in range(n - 1, -1, -1):
        curr = head
        for _ in range(i):
            curr = curr.next
        print(curr.data, end=" ")
    print()

# Q7_2
import math


def traverse_reverse_sqrt(head: Node) -> None:
    # 1. 计算长度
    n = 0
    curr = head
    while curr:
        n += 1
        curr = curr.next

    if n == 0:
        return

    b = math.ceil(math.sqrt(n))

    # 2. 收集各块起始节点的指针，使用 O(sqrt(n)) 空间
    block_heads = []
    curr = head
    idx = 0
    while curr:
        if idx % b == 0:
            block_heads.append(curr)
        curr = curr.next
        idx += 1

    # 3. 逆序遍历块，并在块内部收集最多 b 个数据后逆序输出
    for block_idx in range(len(block_heads) - 1, -1, -1):
        block_nodes = []
        curr = block_heads[block_idx]
        count = 0
        while curr and count < b:
            block_nodes.append(curr.data)
            curr = curr.next
            count += 1
        for val in reversed(block_nodes):
            print(val, end=" ")
    print()
# Q8

def generate_permutations(n: int) -> list[list[int]]:
    nums = list(range(1, n + 1))
    result = []

    def backtrack(first: int):
        if first == n:
            result.append(nums[:])
            return
        for i in range(first, n):
            # 交换元素
            nums[first], nums[i] = nums[i], nums[first]
            # 递归填入下一个位置
            backtrack(first + 1)
            # 回溯复原
            nums[first], nums[i] = nums[i], nums[first]

    backtrack(0)
    return result

#Q9

class EfficientSinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value: int) -> None:
        """在链表末尾追加元素: O(1)"""
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def delete(self, value: int) -> bool:
        """删除第一个值为 value 的节点: O(n)"""
        if not self.head:
            return False

        # 如果删除的是头节点
        if self.head.data == value:
            if self.head == self.tail:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
            return True

        curr = self.head
        while curr.next and curr.next.data != value:
            curr = curr.next

        if curr.next:
            # 如果删除的是尾节点
            if curr.next == self.tail:
                self.tail = curr
            curr.next = curr.next.next
            return True

        return False  # 未找到该值

    def findMiddle(self):
        """获取中间节点的值（偶数长度返回中偏右节点）: O(n)"""
        if not self.head:
            return None

        slow = self.head
        fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow.data

    def reverse(self) -> None:
        """就地反转链表: O(n)"""
        if not self.head or not self.head.next:
            return

        prev = None
        curr = self.head
        self.tail = self.head  # 原头节点变为新尾节点

        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        self.head = prev  # 新头节点为原尾节点



if __name__ == '__main__':
    print("--- 步骤 2 & 3: 生成链表 ---")
    print_singly_list(singly_head)
    print_doubly_list(doubly_head)

    print("\n--- 步骤 4: 测试问题 5 的单链表删除功能 ---")
    # 测试删除头节点
    target_head_name = singly_head.data
    singly_head = delete_node_by_value(singly_head, target_head_name)
    print_singly_list(singly_head)

    # 测试删除不存在的节点
    singly_head = delete_node_by_value(singly_head, "NonExistentName")
    print_singly_list(singly_head)

    # 测试删除中间节点
    if singly_head and singly_head.next:
        target_mid_name = singly_head.next.data
        singly_head = delete_node_by_value(singly_head, target_mid_name)
        print_singly_list(singly_head)