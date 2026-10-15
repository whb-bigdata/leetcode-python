"""COMP9123 Assignment 2 Q2: 用 AVL 树实现双端优先队列（DEPQ）。

与 assignment2_2.docx 对应的五个操作：
    insert(k), findMin(), findMax(), removeMin(), removeMax()
保留原文件的 Python 命名 find_min / find_max / remove_min / remove_max。
空队列查询、删除返回 None（伪代码中的 NIL）；重复键抛出 ValueError。

T 到底是什么？
    T = AVLDoubleEndedPriorityQueue() 创建一个管理整棵树的对象。
    T.root 指向根节点；T.min_node / T.max_node 指向极值节点；T.n 是节点数。
    _AVLNode 是一个实际节点，保存 key / left / right / parent / height。
    T 不是根节点，也不复制一份树：这些属性只是对已有节点的引用。
    T.insert(k) 中的 self 就是 T；辅助函数 avl_insert(self, k) 接收同一个对象。

伪代码与 Python 的对应：
    AVL-INSERT(T, k)       -> avl_insert(T, k)
    AVL-DELETE(T, v)       -> avl_delete(T, v)（仅删除极值节点）
    AVL-REBALANCE-AT(T, p) -> avl_rebalance_at(T, p)
    ROTATE-LEFT(T, x)      -> rotate_left(T, x)
    ROTATE-RIGHT(T, x)     -> rotate_right(T, x)
Python 用缩进结束 if / while / 函数块，不写 end if / end while。

正确性要点：搜索和旋转保持 BST 顺序，向上回溯恢复 AVL 高度和平衡。
最小节点没有左孩子；由 AVL 平衡可知，它的右孩子若存在只能是叶子，
所以其后继是右孩子，或（无右孩子时）父节点。最大节点的前驱对称。
删除直接摘除节点，不复制键；旋转仅改变链接，因此极值引用保持有效。

复杂度（按题目的基本操作为 O(1) 的模型）：查询极值 O(1)，插入和删除
最坏 O(log n)，空树/单节点操作 O(1)。五个操作迭代回溯，辅助空间 O(1)，
全部节点占 O(n)。inorder() 仅用于演示，输出 O(n)，递归栈 O(log n)。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(eq=False)
class _AVLNode:
    """一个节点；eq=False 使节点按身份区分，不递归比较父子链接。"""

    key: int
    left: Optional[_AVLNode] = None
    right: Optional[_AVLNode] = None
    height: int = 1
    parent: Optional[_AVLNode] = None


class AVLDoubleEndedPriorityQueue:
    """整棵 AVL 树及其极值缓存；外部可把这个对象命名为 T。"""

    def __init__(self) -> None:
        # T = AVLDoubleEndedPriorityQueue() 时自动执行；此时尚无节点。
        self.root: Optional[_AVLNode] = None
        self.min_node: Optional[_AVLNode] = None
        self.max_node: Optional[_AVLNode] = None
        self.n = 0

    def insert(self, key: int) -> None:
        """insert(k)：先插入并恢复平衡，再更新极值缓存和节点数。"""
        v = avl_insert(self, key)  # self 就是调用 T.insert(key) 的 T。
        if self.n == 0:
            self.min_node = v
            self.max_node = v
        else:
            assert self.min_node is not None and self.max_node is not None
            if key < self.min_node.key:
                self.min_node = v
            if key > self.max_node.key:
                self.max_node = v
        self.n += 1

    def find_min(self) -> Optional[int]:
        """findMin()：直接访问缓存，O(1)。"""
        if self.min_node is None:
            return None
        return self.min_node.key

    def find_max(self) -> Optional[int]:
        """findMax()：直接访问缓存，O(1)。"""
        if self.max_node is None:
            return None
        return self.max_node.key

    def remove_min(self) -> Optional[int]:
        """removeMin()：提前保存后继引用，再摘除最小节点并恢复平衡。"""
        if self.n == 0:
            return None
        v = self.min_node
        assert v is not None
        key = v.key
        if self.n == 1:
            self.root = self.min_node = self.max_node = None
            self.n = 0
            return key

        # 这个 O(1) 后继规则依赖 AVL 平衡，不适用于任意 BST。
        if v.right is not None:
            new_min = v.right
        else:
            new_min = v.parent
        avl_delete(self, v)
        self.min_node = new_min
        self.n -= 1
        return key

    def remove_max(self) -> Optional[int]:
        """removeMax()：与删除最小值对称。"""
        if self.n == 0:
            return None
        v = self.max_node
        assert v is not None
        key = v.key
        if self.n == 1:
            self.root = self.min_node = self.max_node = None
            self.n = 0
            return key

        if v.left is not None:
            new_max = v.left
        else:
            new_max = v.parent
        avl_delete(self, v)
        self.max_node = new_max
        self.n -= 1
        return key

    # 同一套实现同时支持报告的名称与原文件的 snake_case 名称。
    findMin = find_min
    findMax = find_max
    removeMin = remove_min
    removeMax = remove_max

    def size(self) -> int:
        return self.n

    def is_empty(self) -> bool:
        return self.n == 0

    def inorder(self) -> List[int]:
        """辅助演示：中序遍历得到有序键列表，不属于题目五个操作。"""
        values: List[int] = []

        def visit(u: Optional[_AVLNode]) -> None:
            if u is not None:
                visit(u.left)
                values.append(u.key)
                visit(u.right)

        visit(self.root)
        return values


def height(u: Optional[_AVLNode]) -> int:
    """height(NIL)=0；直接读取缓存高度，不遍历子树。"""
    return 0 if u is None else u.height


def avl_insert(T: AVLDoubleEndedPriorityQueue, k: int) -> _AVLNode:
    """内部步骤：插入并重平衡，返回新节点 v；不更新 n 或极值缓存。"""
    p = None
    u = T.root
    while u is not None:
        p = u
        if k == u.key:
            # 题目假设键互异；保留原实现的重复键检查，且不修改树。
            raise ValueError("duplicate keys are not supported")
        if k < u.key:
            u = u.left
        else:
            u = u.right

    v = _AVLNode(key=k, parent=p)  # height=1，left/right=None。
    if p is None:
        T.root = v
    elif k < p.key:
        p.left = v
    else:
        p.right = v

    while p is not None:
        # 更新高度已包含在 avl_rebalance_at 的第一步中。
        r = avl_rebalance_at(T, p)
        p = r.parent  # 从修复后的局部根继续向上，不能沿旧 p 再走一遍。
    return v  # 返回插入的节点，而不是旋转后的根。


def avl_delete(T: AVLDoubleEndedPriorityQueue, v: _AVLNode) -> None:
    """内部步骤：只删除 T 的极值节点；外层方法负责 n 和极值缓存。"""
    if v is not T.min_node and v is not T.max_node:
        raise ValueError("avl_delete only supports extreme nodes of T")
    p = v.parent
    if v.left is not None:
        child = v.left
    else:
        child = v.right

    if p is None:
        T.root = child
    elif p.left is v:
        p.left = child
    else:
        p.right = child
    if child is not None:
        child.parent = p

    v.left = v.right = v.parent = None
    while p is not None:
        r = avl_rebalance_at(T, p)
        p = r.parent  # 删除后可能有多层失衡，要一直检查到根。


def avl_rebalance_at(T: AVLDoubleEndedPriorityQueue, p: _AVLNode) -> _AVLNode:
    """修复 p 这一层，返回修复后的局部根；每次至多两次旋转，O(1)。"""
    p.height = 1 + max(height(p.left), height(p.right))
    balance = height(p.left) - height(p.right)
    if balance > 1:
        assert p.left is not None
        if height(p.left.left) < height(p.left.right):
            rotate_left(T, p.left)  # LR：第一次针对左孩子。
        return rotate_right(T, p)  # LL 单旋；LR 的第二次针对 p。
    if balance < -1:
        assert p.right is not None
        if height(p.right.right) < height(p.right.left):
            rotate_right(T, p.right)  # RL：第一次针对右孩子。
        return rotate_left(T, p)  # RR 单旋；RL 的第二次针对 p。
    # 删除时孩子的 balance 可能为 0；上述严格 < 判断使其使用单旋。
    return p


def rotate_left(T: AVLDoubleEndedPriorityQueue, x: _AVLNode) -> _AVLNode:
    """ROTATE-LEFT(T,x)：右孩子 y 上来，x 下去成为 y 的左孩子。"""
    y = x.right
    assert y is not None
    parent = x.parent

    # y 接替 x 原来的位置；若 x 原来是整棵树的根，必须改 T.root。
    y.parent = parent
    if parent is None:
        T.root = y
    elif parent.left is x:
        parent.left = y
    else:
        parent.right = y

    x.right = y.left  # y 原来的左子树交给 x。
    if x.right is not None:
        x.right.parent = x
    y.left = x
    x.parent = y

    # 先更新下面的 x，再更新上面的 y（y 的新高度依赖 x）。
    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))
    return y


def rotate_right(T: AVLDoubleEndedPriorityQueue, x: _AVLNode) -> _AVLNode:
    """ROTATE-RIGHT(T,x)：左孩子 y 上来，x 下去成为 y 的右孩子。"""
    y = x.left
    assert y is not None
    parent = x.parent

    y.parent = parent
    if parent is None:
        T.root = y
    elif parent.left is x:
        parent.left = y
    else:
        parent.right = y

    x.left = y.right
    if x.left is not None:
        x.left.parent = x
    y.right = x
    x.parent = y

    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))
    return y


def _demo() -> None:
    """直接运行本文件，观察 T、根节点以及五个操作的实际结果。"""
    T = AVLDoubleEndedPriorityQueue()
    original_T = T  # 两个名字指向同一个对象，不是复制树。
    print("创建 T 后：root =", T.root, "节点数 =", T.n)
    for k in (10, 20, 30):
        T.insert(k)
        assert T.root is not None
        print(f"插入 {k}：根 = {T.root.key}，T 还是原对象 = {T is original_T}")
    assert T.root is not None and T.root.key == 20
    print("T 是管理对象；T.root 是节点；两者不同：", T is not T.root)
    print("findMin() =", T.findMin(), "findMax() =", T.findMax())
    print("removeMin() =", T.removeMin(), "removeMax() =", T.removeMax())
    print("剩余键值：", T.inorder(), "节点数：", T.size())
    assert T.removeMin() == 20 and T.is_empty()
    print("清空后：root =", T.root, "findMin() =", T.findMin(),
          "removeMax() =", T.removeMax())

    for case, keys in (("LL 右旋", (30, 20, 10)),
                       ("RR 左旋", (10, 20, 30)),
                       ("LR 先左后右", (30, 10, 20)),
                       ("RL 先右后左", (10, 30, 20))):
        tree = AVLDoubleEndedPriorityQueue()
        for k in keys:
            tree.insert(k)
        assert tree.root is not None and tree.root.key == 20
        assert tree.inorder() == [10, 20, 30]
        print(f"{case}：插入 {keys} -> 根 {tree.root.key}，中序 {tree.inorder()}")
    print("AVL DEPQ examples passed.")


if __name__ == "__main__":
    _demo()
