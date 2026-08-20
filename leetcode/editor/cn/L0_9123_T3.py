from L0_9123_node import Node

def print_singly_list(head: Node) -> None:
    """打印单链表"""
    curr = head
    elements = []
    while curr:
        elements.append(str(curr.data))
        curr = curr.next
    print("singly_list: " + (" -> ".join(elements) if elements else "empty"))
