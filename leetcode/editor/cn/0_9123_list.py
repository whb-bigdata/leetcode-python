# ==========================================
# 1.1 用 list 实现【栈 (Stack)】—— 后进先出 LIFO
# ==========================================
print("--- List 实现 Stack ---")
stack = []

# 入栈 (Push) - O(1)
stack.append("页面 A")
stack.append("页面 B")
stack.append("页面 C")
print("入栈后:", stack)  # ['页面 A', '页面 B', '页面 C']

# 查看栈顶 (Peek) - O(1)
if stack:
    top_item = stack[-1]
    print("查看栈顶:", top_item)  # 页面 C

# 出栈 (Pop) - O(1)
popped_item = stack.pop()
print("出栈元素:", popped_item)  # 页面 C
print("出栈后:", stack)  # ['页面 A', '页面 B']

# 判断是否为空 & 获取大小
print("栈大小:", len(stack))
print("栈是否为空:", len(stack) == 0)


# ==========================================
# 1.2 用 list 实现【队列 (Queue)】—— 先进先出 FIFO
# ⚠️ 注意：仅作演示，工程中请勿使用，pop(0) 性能差 O(n)
# ==========================================
print("\n--- List 实现 Queue (不推荐) ---")
queue_list = []

# 入队 (Enqueue) - O(1)
queue_list.append("顾客 1")
queue_list.append("顾客 2")
queue_list.append("顾客 3")
print("入队后:", queue_list)  # ['顾客 1', '顾客 2', '顾客 3']

# 查看队头 (Peek) - O(1)
if queue_list:
    front_item = queue_list[0]
    print("查看队头:", front_item)  # 顾客 1

# 出队 (Dequeue) - ⚠️ O(n) 极其低效！
dequeued_item = queue_list.pop(0)
print("出队元素:", dequeued_item)  # 顾客 1
print("出队后:", queue_list)  # ['顾客 2', '顾客 3']