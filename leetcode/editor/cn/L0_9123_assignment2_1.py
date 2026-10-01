"""COMP9123 Assignment 2: Maximum Ancestor–Descendant Difference.

题目 / Problem
--------------
在整数二叉树中，求任意节点与其祖先之间的最大绝对差。
Find the maximum absolute difference between a node and one of its ancestors.
这是一棵普通二叉树，不要求是二叉搜索树 / The tree need not be a BST.

算法 / Algorithm
----------------
递归先序 DFS，与中文答案的两段伪代码一致。
Recursive preorder DFS, matching the two algorithms in the written solution.
每次调用传入当前路径的 min_ancestor 和 max_ancestor；用 nonlocal
共享本次求解的 max_diff，对应伪代码中的按引用参数。
Path bounds are local to each call; nonlocal shares the current answer.
根以自身值初始化，比较结果为 0；非根节点的边界来自严格祖先。
The root is an initialization exception; non-root bounds are strict ancestors.
先比较当前节点，再更新范围，分别递归左右孩子，不能混用分支极值。
Compare first, extend the bounds, then recurse into left and right children.

复杂度 / Complexity
-------------------
时间 O(n)：非空树有 n 次实际节点调用和 n+1 次空节点调用。
Time O(n): n real-node calls and n+1 null-child calls for a nonempty tree.
辅助空间 O(h)：递归调用栈，h 为最长根到叶路径上的节点数。
Auxiliary space O(h): recursion depth, with height measured in nodes.
Python 有递归深度限制，过深的树可能抛出 RecursionError。
Very deep trees may exceed Python's recursion limit. This module does not
change the interpreter's recursion limit.
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
    python3 L0_9123_assignment2_1.py

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
    """返回最大祖先差值；空树及单节点返回 0。

    Correctness / 正确性：
    非根调用的两个边界恰好是其严格祖先的极值。根调用仅产生差值 0。
    每次先计算当前差值，再将当前值合并到传给孩子的边界，保持不变量。
    对固定节点值，最大祖先差值在祖先最小值或最大值处取得。
    max_diff 汇总所有节点候选，因此最终是全树答案。

    Each non-root call receives exactly its strict-ancestor extrema.
    The root contributes zero. Extending bounds preserves the invariant.
    The farthest ancestor is at an extreme; max_diff aggregates all candidates.
    """
    if root is None:
        return 0

    max_diff = 0

    def dfs_ancestor_diff(
        u: TreeNode | None, min_ancestor: int, max_ancestor: int
    ) -> None:
        # 对应伪代码 ref max_diff；每次外层调用拥有独立的答案。
        # Equivalent to ref max_diff, scoped to this invocation only.
        nonlocal max_diff
        if u is None:
            return

        diff1 = abs(u.value - min_ancestor)
        diff2 = abs(u.value - max_ancestor)
        max_diff = max(max_diff, diff1, diff2)

        new_min = min(min_ancestor, u.value)
        new_max = max(max_ancestor, u.value)
        dfs_ancestor_diff(u.left, new_min, new_max)
        dfs_ancestor_diff(u.right, new_min, new_max)

    dfs_ancestor_diff(root, root.value, root.value)
    return max_diff


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

    # 有界深度链验证；递归版本不再声称支持任意深度。
    # A moderate chain within the normal Python recursion limit.
    root = TreeNode(0)
    current = root
    for value in range(1, 200):
        current.right = TreeNode(value)
        current = current.right
    assert max_ancestor_difference(root) == 199
    # 每次求解重新初始化 max_diff，不能保留上一次调用的结果。
    assert max_ancestor_difference(TreeNode(42)) == 0
    print("200 节点链 / Chain: 199 (expected 199)")

    # 手工跟踪示例 1 的路径 8 -> 3 -> 1 / Trace the path 8 -> 3 -> 1:
    # 当前节点 / node | 祖先范围 / ancestor bounds | 当前候选 / candidate
    #        8        |       [8, 8]（根特例）   |          0
    #        3        |       [8, 8]              |          5
    #        1        |       [3, 8]              |          7
    # 右分支节点 10 从自己的递归参数取得 [8, 8]，不会得到左分支的值 1。
    # Node 10 receives [8, 8] from its own recursive arguments, never the left branch's 1.
    print("All examples passed. / 所有示例检查通过。")


if __name__ == "__main__":
    run_examples()
