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


if __name__ == '__main__':
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    traverse(n1)