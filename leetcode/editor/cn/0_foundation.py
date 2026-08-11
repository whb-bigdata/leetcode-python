#   基础数据结构&使用方法
#   数字


#   字符串
s = '1304328'
print(s)

#   分数
f = 4.356
print(f)


# boolean

t = True
f = False
print(t)
print(f)


#   array Java 数组，无装箱开销，内存极紧凑，类型统一，高密度的纯数值计算、字节流、大矩阵运算
# 2. Python 原生的 array（必须 import array）
import array
n_array = array.array('i', [1, 2, 3, 4, 5])  # 'i' 代表强类型整型
print(type(n_array))  # 输出: <class 'array.array'>


#   list  Java ArrayList<Object>，动态指针数组，按索引随机访问极快 ($O(1)$)，默认首选、通用列表、栈（Stack）、算法题中 90% 的场景
nums = [1, 2, 3]
print(len(nums))  # 输出 3
for n in nums:    # 正常运行
    print(n,1,sep='?', end=' ')
nums.append(4)
print('\n-----')
l = len(nums)
print(l)
n2 = nums[2]
print(n2)
print(nums)
nums.pop(2)
print(nums)
n = [1, 2, 3, 4, 5]
print(type(n))

#deque Java LinkedList

from collections import deque

# 创建双向链表/双端队列（相当于 Java 的 LinkedList / ArrayDeque）双向块状链表，头尾插入和弹出极快 ($O(1)$)，队列（Queue）、BFS（广度优先搜索）、滑动窗口
queue = deque([1, 2, 3])
print(type(queue))
queue.appendleft(0)  # 头部插入 O(1)，相当于 Java 的 linkedList.addFirst(0)
queue.appendleft(4)  # 头部插入 O(1)，相当于 Java 的 linkedList.addFirst(0)
queue.append(4)      # 尾部插入 O(1)，相当于 Java 的 linkedList.addLast(4)

left_val = queue.popleft()  # 头部弹出 O(1)，相当于 Java 的 linkedList.pollFirst()
print(left_val)
print(queue)

#   set

# 1. 创建 (注意：空集合必须用 set()，不能用 {})
my_set = set()
# 也可以初始化赋值: my_set = {1, 2, 3}

# --- 2. 插入 ---
my_set.add(10)               # 相当于 Java 的 set.add(10)
my_set.add(20)
my_set.update([30, 40, 50])  # 批量插入多个元素

for item in my_set:
    print(item)
# --- 3. 删除 / 弹出 ---
my_set.remove(10)            # 删除元素，若元素不存在则抛出 KeyError
my_set.discard(99)           # 推荐！安全删除：若元素存在则删除，不存在也不报错

popped_val = my_set.pop()    # 随机弹出并返回集合中的任意一个元素（无序）

# --- 4. 存在性检查 ---
if 20 in my_set:             # 相当于 Java 的 set.contains(20)，O(1) 时间复杂度
    print("20 在集合中")


#   map

# 1. 创建 (注意：{} 表示空字典，而不是空集合)
my_map = {}
# 也可以初始化赋值: my_map = {"apple": 5, "banana": 3}

# --- 2. 插入 / 修改 ---
my_map["apple"] = "banana"
my_map["pear"] = "orange"

# --- 3. 查找与获取 ---
val1 = my_map["apple"]              # 直接用 key 获取，如果 key 不存在会抛出 KeyError 异常
val2 = my_map.get("pear", 0)        # 强烈推荐！相当于 Java 的 map.getOrDefault("pear", 0)

if "apple" in my_map:               # 相当于 Java 的 map.containsKey("apple")
    print("Key 存在")
    print(my_map["apple"])
# --- 4. 删除 / 弹出 ---
val = my_map.pop("apple")           # 弹出指定 key，返回对应 value，相当于 Java 的 map.remove("apple")
val_safe = my_map.pop("pear1", "None") # 安全弹出：如果 key 不存在则返回默认值 None，不会报错
print(val)
print(val_safe)
del my_map["banana"]                # 直接删除 key（无返回值，如果 key 不存在会报错）

scores = {'A':22,'B':44,'C':77}

# 1. 遍历 Key-Value（最常用，相当于遍历 map.entrySet()）
for name, score in scores.items():
    print(f"{name}: {score}")

# 2. 仅遍历 Key（相当于遍历 map.keySet()）
for name in scores:         # 也可以写成 for name in scores.keys():
    print(name)

# 3. 仅遍历 Value（相当于遍历 map.values()）
for score in scores.values():
    print(score)