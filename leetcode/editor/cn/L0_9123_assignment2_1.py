"""COMP9123 Assignment 2: Maximum Ancestor–Descendant Difference.

题目 / Problem
--------------
在整数二叉树中，求任意节点与其祖先之间的最大绝对差。
Find the maximum absolute difference between a node and one of its ancestors.
这是一棵普通二叉树，不要求是二叉搜索树 / The tree need not be a BST.

算法 / Algorithm
----------------
迭代深度优先遍历（DFS）。每个栈项保存：
    (当前节点 / node, 祖先最小值 / ancestor_min, 祖先最大值 / ancestor_max)
沿路径向下传递最小值和最大值，不重复向上查找祖先。
Pass the path minimum and maximum down the tree instead of walking upwards.

对值为 v 的节点，只需要检查 / For a node with value v, only check:
    max(abs(v - ancestor_min), abs(v - ancestor_max))

两个孩子分别获得包含当前节点的新范围；不能将不同分支的最值混用。
Each child receives the updated range for its own ancestor path.
Never combine the extrema from unrelated branches.

复杂度 / Complexity
-------------------
时间 O(n)：每个节点入栈、出栈各一次，每次处理只做常数次运算。
Time O(n): each node is pushed and popped once, with constant work per node.
额外空间 O(h)：DFS 栈仅保存当前路径旁尚未访问的分支，h 是树高。
Auxiliary space O(h): the DFS stack holds pending branches along a path.
这里高度按路径中的节点数计算；最坏 O(h) <= O(n)。实际栈可能更小。
Height counts nodes on a root-to-leaf path; actual stack use can be smaller.
按通常的算法分析模型，将整数比较和算术操作视为 O(1)。
As usual, integer comparisons and arithmetic are treated as constant time.

边界约定 / Edge-case convention
-----------------------------
空树或只有一个节点时，不存在严格祖先–后代对，本实现约定返回 0。
An empty or single-node tree has no strict ancestor–descendant pair; return 0.
输入应为无环、无共享子节点的有限二叉树，不是任意图。
The input must be a finite tree without cycles or shared child nodes.

运行 / Run (Python 3.10+)
-----------------------
    python3 L0_9123_assignment2.py

无第三方依赖。导入时不会运行示例。
No third-party packages. Importing this module does not run the examples.
"""

from __future__ import annotations


class TreeNode:
    """二叉树节点 / A binary tree node.

    value（节点值 / node value）：整数 / an integer.
    left（左孩子 / left child）：TreeNode 或 None.
    right（右孩子 / right child）：TreeNode 或 None.
    """

    def __init__(
        self,
        value: int,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right


def max_ancestor_difference(root: TreeNode | None) -> int:
    """返回最大祖先–后代绝对差 / Return the maximum ancestor difference.

    root（根节点 / root node）：二叉树根；None 表示空树。
    返回 / Returns：最大的绝对差；没有有效节点对时为 0。

    正确性 / Correctness
    --------------------
    1. 路径不变量：非根节点出栈时，ancestor_min 和 ancestor_max
       恰好是其所有严格祖先值的最小值和最大值。
       Path invariant: for a non-root node, the stored bounds are exactly
       the minimum and maximum over its strict ancestors.

       根是特殊初始项，以自身值作为两个边界，只产生差值 0。
       处理后把当前值合并到边界，传给两个孩子，因而不变量成立。
       The root is a special initial entry, contributing only zero.
       Including the current value before pushing its children preserves
       the invariant, because the current node is an ancestor of each child.

    2. 对当前值 v，离它最远的祖先值一定可以在上述两个端点中找到。
       两端点都来自真实祖先，因此该节点的候选差值既不会漏掉最大值，
       也不会把其他分支中不属于祖先的节点算进去。
       For a fixed v, the largest |v-a| over ancestor values a is attained
       at their minimum or maximum. Both bounds come from actual ancestors.

    3. best 是所有已处理节点候选差值的最大值。遍历覆盖全部节点，
       所以结束时 best 就是整棵树的答案。
       best is the maximum candidate among processed nodes. DFS visits
       every node, so the final best is the required global maximum.

    空间说明：二叉树 DFS 每层至多留下一个尚未探索的兄弟分支，
    再加当前待处理项，栈长度为 O(h)。不存整条祖先列表，也不递归。
    At most one pending sibling per level plus the current entry gives
    O(h) stack space. No ancestor-list copies or recursion are needed.
    """
    if root is None:
        return 0

    best = 0
    # 元组中的整数范围属于这一条路径；不会被另一分支的更新覆盖。
    # Each tuple owns the bounds for its path; branches do not share updates.
    stack = [(root, root.value, root.value)]

    while stack:
        node, ancestor_min, ancestor_max = stack.pop()

        # 先与祖先比较，再将当前值加入传给孩子的范围。
        # Compare with ancestors before extending the range for the children.
        best = max(
            best,
            abs(node.value - ancestor_min),
            abs(node.value - ancestor_max),
        )
        path_min = min(ancestor_min, node.value)
        path_max = max(ancestor_max, node.value)

        # 后进先出：先压右孩子，使左孩子先处理；顺序不影响结果。
        # Push right first to visit left first. Either DFS order is valid.
        if node.right is not None:
            stack.append((node.right, path_min, path_max))
        if node.left is not None:
            stack.append((node.left, path_min, path_max))

    return best


def run_examples() -> None:
    """构建示例树、调用算法并检查答案 / Build trees and check the results."""
    # 示例 1 / Example 1:
    #          8
    #        /   \
    #       3     10
    #      / \      \
    #     1   6      14
    #        / \     /
    #       4   7   13
    # 最大差来自祖先 8 和后代 1：|8 - 1| = 7。
    # The maximum is between ancestor 8 and descendant 1.
    example = TreeNode(
        8,
        TreeNode(3, TreeNode(1), TreeNode(6, TreeNode(4), TreeNode(7))),
        TreeNode(10, right=TreeNode(14, left=TreeNode(13))),
    )

    cases = [
        ("普通二叉树 / Example tree", example, 7),
        ("空树 / Empty tree", None, 0),
        ("单节点 / Single node", TreeNode(42), 0),
        ("相同值 / Equal values", TreeNode(5, TreeNode(5), TreeNode(5)), 0),
        # 1 和 9 是兄弟，不是祖先与后代；不能返回全树最大值减最小值 8。
        # Siblings 1 and 9 are not an ancestor–descendant pair; answer is 4, not 8.
        ("不能跨分支比较 / No cross-branch pairs", TreeNode(5, TreeNode(1), TreeNode(9)), 4),
        # 最大差不一定包含根：这条链上 1 是 9 的祖先，|1 - 9| = 8。
        # The best pair need not include the root: ancestor 1 and descendant 9.
        ("非根祖先 / Non-root ancestor", TreeNode(5, left=TreeNode(1, left=TreeNode(9))), 8),
        ("含负数 / Negative values", TreeNode(-10, TreeNode(-20), TreeNode(-3, right=TreeNode(-40))), 37),
        ("正负混合 / Mixed signs", TreeNode(-10, right=TreeNode(10)), 20),
    ]

    for name, root, expected in cases:
        actual = max_ancestor_difference(root)
        assert actual == expected, f"{name}: expected {expected}, got {actual}"
        print(f"{name}: {actual} (expected {expected})")

    # 深链验证：0 -> 1 -> ... -> 4999，不使用递归，不依赖递归深度限制。
    # A deep chain is processed iteratively without hitting recursion limits.
    root = TreeNode(0)
    current = root
    for value in range(1, 5000):
        current.right = TreeNode(value)
        current = current.right
    actual = max_ancestor_difference(root)
    assert actual == 4999
    print(f"5000 节点深链 / Deep chain: {actual} (expected 4999)")

    # 手工跟踪示例 1 的路径 8 -> 3 -> 1 / Trace the path 8 -> 3 -> 1:
    # 当前节点 / node | 祖先范围 / ancestor bounds | 当前候选 / candidate
    #        8        |       [8, 8]（根特例）     |          0
    #        3        |       [8, 8]              |          5
    #        1        |       [3, 8]              |          7
    # 右分支节点 10 从自己的栈项取得 [8, 8]，不会得到左分支的值 1。
    # Node 10 receives [8, 8] from its own stack entry, never the left branch's 1.
    print("All examples passed. / 所有示例检查通过。")


if __name__ == "__main__":
    run_examples()
