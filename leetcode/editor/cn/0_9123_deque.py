from collections import deque

# ==========================================
# 2.1 用 deque 实现【栈 (Stack)】—— 后进先出 LIFO
# ==========================================
print("--- Deque 实现 Stack ---")
deque_stack = deque()

# 入栈 (Push) - O(1)
deque_stack.append(10)
deque_stack.append(20)
deque_stack.append(30)
print("入栈后:", deque_stack)  # deque([10, 20, 30])

# 查看栈顶 (Peek) - O(1)
if deque_stack:
    print("查看栈顶:", deque_stack[-1])  # 30

# 出栈 (Pop) - O(1)
popped = deque_stack.pop()
print("出栈元素:", popped)  # 30
print("出栈后:", deque_stack)  # deque([10, 20])


# ==========================================
# 2.2 用 deque 实现【队列 (Queue)】—— 先进先出 FIFO (推荐做法)
# ==========================================
print("\n--- Deque 实现 Queue (推荐) ---")
deque_queue = deque()

# 入队 (Enqueue) - O(1)
deque_queue.append("任务 1")
deque_queue.append("任务 2")
deque_queue.append("任务 3")
print("入队后:", deque_queue)  # deque(['任务 1', '任务 2', '任务 3'])

# 查看队头 (Peek) - O(1)
if deque_queue:
    print("查看队头:", deque_queue[0])  # 任务 1

# 出队 (Dequeue) - O(1) 使用 popleft() 弹出队头
dequeued = deque_queue.popleft()
print("出队元素:", dequeued)  # 任务 1
print("出队后:", deque_queue)  # deque(['任务 2', '任务 3'])

# 判断是否为空
print("队列是否为空:", len(deque_queue) == 0)