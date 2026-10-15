"""COMP9123 Tutorial 10: Greedy Algorithms / 贪心算法。

来源 / Source: T10_COMP9123_W10_Greedy_Algorithms.pdf, Problems 1-8.
原 PDF 页眉标注 s2 2025；这里按照用户提供的这份原文作答。

题目安排 / Contents:
    1      Huffman 树：可运行代码、字符频率、编码和树形输出。
    2-5    理论题：中英文关键解答、反例和正确性证明。
    6      最少单位长度区间覆盖：算法、证明和复杂度。
    7 a-c  最小加权完成时间：算法、相邻交换证明和复杂度。
    8 a-c  买花最小总价：算法、分配方案、证明和复杂度。

运行 / Run: python3 L0_9123_T10.py
导入时不会运行示例 / Importing this module does not run the examples.
依赖 / Dependencies: 仅 Python 标准库 collections、dataclasses、fractions、
heapq、itertools；无需安装第三方包。需要 Python 3.10+。
所有排序都创建副本，不改变调用者的列表。复杂度采用通常的单位代价算术模型；
Python 大整数和 Fraction 的实际运算成本还取决于数字的位数。
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from heapq import heapify, heappop, heappush
from itertools import count


Number = int | float | Fraction


# ---------------------------------------------------------------------------
# Problem 1 / 第 1 题：为 "data structure" 构造 Huffman 树
# ---------------------------------------------------------------------------
@dataclass
class HuffmanNode:
    """Huffman 节点 / A leaf has a symbol; an internal node has two children."""

    frequency: int
    symbol: str | None = None
    left: HuffmanNode | None = None
    right: HuffmanNode | None = None


def build_huffman_tree(text: str) -> HuffmanNode | None:
    """构造 Huffman 树 / Build a minimum-weight prefix-code tree.

    中文：空格也是字符；每次合并当前频率最小的两棵树。同频率时使用序号
    打破并列，避免比较节点对象。空文本返回 None，单字符文本返回一个叶子。
    正确性关键：存在一棵最优树，使最小的两个频率成为最深层的兄弟叶子；
    将它们收缩为一个权重等于两者之和的节点，就得到相同类型的子问题。

    English: Include spaces. Repeatedly merge the two least-frequent trees.
    A serial number resolves ties without comparing node objects. There is an
    optimal tree whose two least-frequent symbols are deepest sibling leaves;
    contracting them gives a smaller instance, establishing the greedy step.
    Ties may produce different trees with the same optimal weighted length.

    m = len(text), k = number of distinct symbols:
    Time O(m + k log k); auxiliary space O(k), including the returned tree.
    """
    frequencies = Counter(text)
    serial = count()
    heap = [
        (frequency, next(serial), HuffmanNode(frequency, symbol))
        for symbol, frequency in frequencies.items()
    ]
    heapify(heap)

    while len(heap) > 1:
        _, _, left = heappop(heap)
        _, _, right = heappop(heap)
        parent = HuffmanNode(left.frequency + right.frequency, left=left, right=right)
        heappush(heap, (parent.frequency, next(serial), parent))

    return heap[0][2] if heap else None


def huffman_codes(root: HuffmanNode | None) -> dict[str, str]:
    """左边记 0，右边记 1 / Label left edges 0 and right edges 1.

    单字符采用编码 "0" 的约定；空树返回空字典。
    A one-symbol alphabet uses "0" by convention; an empty tree has no codes.
    输出编码的总长度为 L 时，生成编码的时间和存储空间为 O(L)。
    Code generation takes O(L) time/space, where L is total code-string length.
    """
    codes = {}
    if root is None:
        return codes

    stack = [(root, "")]
    while stack:
        node, prefix = stack.pop()
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"
        else:
            assert node.left is not None and node.right is not None
            stack.append((node.right, prefix + "1"))
            stack.append((node.left, prefix + "0"))
    return codes


def print_huffman_tree(root: HuffmanNode | None) -> None:
    """用缩进打印树；0/1 是边标签 / Print the tree with labelled edges."""
    if root is None:
        print("(empty tree / 空树)")
        return

    stack = [(root, 0, "root")]
    while stack:
        node, depth, edge = stack.pop()
        label = repr(node.symbol) if node.symbol is not None else "internal"
        print(f"{'    ' * depth}{edge}: {label}, frequency={node.frequency}")
        if node.symbol is None:
            assert node.left is not None and node.right is not None
            stack.append((node.right, depth + 1, "1"))
            stack.append((node.left, depth + 1, "0"))


# ---------------------------------------------------------------------------
# Problems 2-5 / 第 2-5 题：原题要求论证，直接提供中英文解答。
# ---------------------------------------------------------------------------
THEORY_ANSWERS = {
    2: """
Problem 2 / 第 2 题：分数背包中两种规则的无限成功实例族

中文：本题不是要求只给失败反例，而是为每种规则构造无限个成功实例。
1. 最高收益优先：对每个整数 n >= 2，令物品 i=1,...,n 的重量
   w_i=1、收益 b_i=i，容量 W=n/2。收益排序就是 b_i/w_i=i 的排序，
   因而与正确的分数背包规则完全一致，得到最优解。
2. 最小重量优先：对每个整数 n >= 2，令 w_i=i、b_i=1，容量 W=n。
   按重量升序就是按收益重量比 1/i 降序，因此同样最优。
两族都有任意大的 n，且容量不足以装下全部物品，允许取一部分物品。
特定输入上成功，即使有无限多个，也不能证明对所有输入都正确。

English: Give an infinite successful family for each rule.
1. Highest benefit first: for every integer n >= 2, take w_i=1, b_i=i
   for i=1,...,n, and capacity W=n/2. Descending benefit is exactly
   descending benefit-to-weight ratio, so the fractional solution is optimal.
2. Smallest weight first: take w_i=i, b_i=1, and capacity W=n for each
   n >= 2. Ascending weight is descending ratio 1/i, so it is optimal.
Both families have unbounded size and cannot fit all items in the knapsack.
Items are divisible. Success on these families does not prove correctness
on all instances.
""",
    3: """
Problem 3 / 第 3 题：greedy-matching-v1 不正确 / Incorrect

中文：取 a=[0,10]，b=[9,20]。四个跨集合距离为 9、20、1、10，
没有并列。贪心先取唯一最近的 (10,9)，再取 (0,20)，总成本 1+20=21。
而匹配 (0,9)、(10,20) 的成本为 9+10=19。n=2 时只有这两种配对，
所以最优值为 19。局部最接近不保证全局总距离最小。

English: Let a=[0,10] and b=[9,20]. The cross-set distances are 9,20,1,10,
with no ties. Greedy picks (10,9), then (0,20), at cost 1+20=21.
The other matching, (0,9),(10,20), costs 9+10=19 and is optimal because
there are only two matchings. Thus the nearest-pair rule is not correct.
""",
    4: """
Problem 4 / 第 4 题：greedy-matching-v2 正确 / Correct

中文：将 a 和 b 分别升序排序，再按相同下标配对。
交换不等式：若 x <= x' 且 y <= y'，则
    |x-y| + |x'-y'| <= |x-y'| + |x'-y|。
证明：令 g(t)=|t-y|-|t-y'|。当 t<=y 时为 y-y'；当 y<=t<=y'
时为 2t-y-y'；当 t>=y' 时为 y'-y。因此 g 单调不减，
g(x)<=g(x')，移项得到不等式。
将任意最优匹配按 a 升序排列；若匹配的 b 序列有相邻逆序，交换
这两个 b 后成本不会增加。反复消除逆序，得到两个序列都升序的匹配，
其成本仍为最优。重复元素不影响证明。排序实现为 O(n log n) 时间，
若保留输入并创建排序副本，额外空间为 O(n)。

English: Sort both vectors ascending and pair equal positions.
For x<=x' and y<=y', the exchange inequality is
    |x-y| + |x'-y'| <= |x-y'| + |x'-y|.
Indeed, g(t)=|t-y|-|t-y'| equals y-y' for t<=y, 2t-y-y' between y and y',
and y'-y for t>=y'. It is nondecreasing, so g(x)<=g(x') implies the inequality.
Order an optimal matching by a. Swap any adjacent inverted b-values;
the inequality shows that cost cannot increase. Eliminating all inversions
produces the sorted matching, so it is optimal. Ties cause no difficulty.
Sorting takes O(n log n) time and O(n) extra space when making sorted copies.
""",
    5: """
Problem 5 / 第 5 题：Huffman 树中每个内部节点至少有一个叶子孩子

中文：原文是 f_i=2**i（指数），不是 2*i，i=1,...,k。
令 S_j=2+4+...+2**j=2**(j+1)-2。
归纳不变量：当前唯一的合并树包含 c_1,...,c_j，重量为 S_j；
其余树都是 c_{j+1},...,c_k 的单叶树。初始将 c_1 视为 S_1=2 的树。
当 j<k 时，S_j < 2**(j+1)，后面的叶子更重。因此当前最小的两棵树
恰好是 S_j 的树和叶子 c_{j+1}；合并得到 S_{j+1}，不变量保持。
首次合并有两个叶子孩子，以后每次新内部节点都带一个新叶子孩子。
所以所有内部节点都至少有一个叶子孩子。k=1 时没有内部节点，结论自然成立。

English: The frequencies are f_i=2**i, not 2*i.
Let S_j=2+4+...+2**j=2**(j+1)-2. Inductively, the only merged tree contains
c_1,...,c_j with weight S_j; the others are the single leaves c_{j+1},...,c_k.
Initially regard c_1 as the S_1=2 tree. For j<k, S_j<2**(j+1), and all
later leaves are heavier. Thus Huffman merges the S_j tree with leaf c_{j+1},
forming S_{j+1} and preserving the invariant. The first parent has two leaf
children; every later new parent has the newly added leaf as a child.
Hence every internal node has at least one leaf child. For k=1 the claim is
vacuously true because there are no internal nodes.
""",
}


# ---------------------------------------------------------------------------
# Problem 6 / 第 6 题：最少单位长度区间覆盖
# ---------------------------------------------------------------------------
def minimum_unit_intervals(points: list[Number]) -> list[tuple[Fraction, Fraction]]:
    """返回最少的单位长度闭区间 / Return a minimum unit-interval cover.

    中文：输入为有限实数点。采用闭区间 [x,x+1]，端点算作被覆盖。
    每次取最左边未覆盖点 x，加入 [x,x+1]，跳过所有不大于 x+1 的点。
    正确性：任意最优解中覆盖 x 的 [a,a+1] 可右移为 [x,x+1]。
    因为剩余点都 >=x，而 x+1>=a+1，不会丢失任何剩余点的覆盖。
    因此存在包含贪心选择的最优解；对未覆盖点重复即可。

    English: Use closed intervals, including endpoints, on finite real points.
    Cover the leftmost uncovered x with [x,x+1]. An optimal interval [a,a+1]
    containing x can be shifted right to [x,x+1] without losing any remaining
    point, since all such points are >=x. Repeating gives an optimal cover.
    Time O(n log n) for sorting plus O(n) scanning; space O(n).
    输入转为 Fraction，返回精确有理数端点，避免大浮点数加 1 后被舍入。
    浮点按实际存储值转换；需要精确小数时可用 Fraction("0.1")。
    Convert inputs to Fraction and return exact rational endpoints so adding 1
    cannot round away. Floats retain their stored values; pass Fraction for
    exact decimal inputs.
    """
    ordered = sorted(Fraction(point) for point in points)
    intervals = []
    i = 0
    while i < len(ordered):
        start = ordered[i]
        end = start + 1
        intervals.append((start, end))
        i += 1
        while i < len(ordered) and ordered[i] <= end:
            i += 1
    return intervals


# ---------------------------------------------------------------------------
# Problem 7 / 第 7 题：最小化 sum(w_j * C_j)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Job:
    """作业 / A job: name=名称, processing_time=处理时间, weight=权重."""

    name: str
    processing_time: Number
    weight: Number


def optimal_job_schedule(jobs: list[Job]) -> list[Job]:
    """按 t/w 升序排序 / Smith's rule: increasing processing_time / weight.

    (a) 中文：所有任务在时间 0 可用、单机、不可抢占、t>0 且 w>0。
    不需要空闲时间。按 t/w 升序处理；相等比率保持原输入顺序即可。
    Fraction 保存精确比率，避免大整数转浮点后两个不同比率变成相同值。
    浮点输入按其存储的二进制数值转换；精确小数可传 Fraction("0.1")。
    English: With all jobs available at zero, run without idle time in ascending
    t/w order. Stable sorting handles ties. Fraction avoids rounded ratio keys;
    finite floats are interpreted as their stored binary values.

    (b) 中文：相邻 i,j 之前已用时间 S。两种顺序的相关成本分别为
      F_ij = w_i*(S+t_i) + w_j*(S+t_i+t_j)
      F_ji = w_j*(S+t_j) + w_i*(S+t_j+t_i)
    交换后的变化 F_ji-F_ij = w_i*t_j-w_j*t_i。
    若 t_i/w_i > t_j/w_j，则变化 <0；相等时为 0。
    其他任务的完成时间不变，因为这两项的总耗时不变。
    反复交换相邻逆序即可得到排序顺序且成本不增，所以该顺序最优。
    English: An adjacent swap changes the objective by
      F_ji-F_ij = w_i*t_j-w_j*t_i.
    This is negative for an inverted ratio pair and zero for a tie. Earlier
    jobs are untouched, and later jobs start at the same time. Removing all
    inversions transforms an optimal schedule into the sorted schedule without
    increasing its cost; hence the sorted schedule is optimal.

    (c) Time O(n log n) comparisons; space O(n). Evaluating the schedule is O(n).
    这里按算术操作计复杂度；大整数/有理数的位运算成本另计。
    Bit complexity additionally depends on the sizes of the rational numbers.
    """
    for job in jobs:
        if not (job.processing_time > 0 and job.weight > 0):
            raise ValueError("Every job needs processing_time > 0 and weight > 0")

    return sorted(
        jobs,
        key=lambda job: Fraction(job.processing_time) / Fraction(job.weight),
    )


def weighted_completion_time(schedule: list[Job]) -> Number:
    """计算给定顺序的目标值 / Evaluate sum(weight * completion_time) in O(n)."""
    elapsed = 0
    total = 0
    for job in schedule:
        elapsed += job.processing_time
        total += job.weight * elapsed
    return total


# ---------------------------------------------------------------------------
# Problem 8 / 第 8 题：买花最小总花费（包含 Challenge）
# ---------------------------------------------------------------------------
def minimum_flower_cost(
    prices: list[Number], k: int
) -> tuple[Number, list[tuple[int, Number, int]]]:
    """返回总价和购买方案 / Return (total_cost, purchases).

    purchases 每项为 (朋友编号, 原价, 倍率)，朋友编号从 1 开始。
    Each purchase is (one-based friend number, original price, multiplier).
    Prices are finite and nonnegative; k is a positive integer.

    (a) 中文：价格降序排列，依次轮流分给 k 个朋友。零基下标 i 的花
    分给朋友 i%k+1，倍率为 i//k+1。这样先使用 k 个 1 倍位，再使用
    k 个 2 倍位，依次类推。重复价格可以任意排序。
    English: Sort prices descending and assign them round-robin. Flower i
    (zero-based) goes to friend i%k+1 with multiplier i//k+1.

    (b) 中文：每位朋友提供倍率 1,2,3,... 的购买位置。若使用了较大的
    倍率，却留有某位朋友下一个较小倍率的位置，将高倍率的最后一次
    购买移过去不会增价。因此可选择所有位置中最小的 n 个倍率。
    对 p>=q、a<=b，(p*b+q*a)-(p*a+q*b)=(p-q)*(b-a)>=0，
    所以较贵的花应配较小倍率。降序价格配递增倍率达到此下界，且轮流
    分配确实能实现这些倍率，因此最优。
    English: Each friend supplies slots with multipliers 1,2,3,... . Moving a
    final purchase from a larger multiplier to an unused smaller next slot
    cannot increase cost. Thus use the n smallest available multipliers.
    For p>=q and a<=b, (p*b+q*a)-(p*a+q*b)=(p-q)*(b-a)>=0.
    Pairing larger prices with smaller multipliers is optimal, and round-robin
    assignment realizes these slots, proving the strategy feasible and optimal.

    (c) Sorting O(n log n), scanning O(n), space O(n) including the purchase plan.
    示例 / Example: [2,5,6,3,8], k=2 -> 8+6+2*5+2*3+3*2 = 36.
    原文例子把交替购买的第五朵记到 Friend 2；严格交替应归 Friend 1，
    但两种写法的总价均为 49，不影响最优值 36。
    The PDF assigns the fifth flower to Friend 2 despite saying alternating
    turns; it would be Friend 1 under strict alternation. Both totals are 49.
    """
    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer")
    if any(not (price >= 0) for price in prices):
        raise ValueError("Flower prices must be nonnegative")

    total = 0
    purchases = []
    for i, price in enumerate(sorted(prices, reverse=True)):
        friend = i % k + 1
        multiplier = i // k + 1
        purchases.append((friend, price, multiplier))
        total += price * multiplier
    return total, purchases


def main() -> None:
    """运行各题示例和基础断言 / Run examples and basic correctness checks."""
    print("Problem 1 / 第 1 题: Huffman tree for 'data structure'")
    text = "data structure"  # 保留中间空格 / Keep the space.
    root = build_huffman_tree(text)
    codes = huffman_codes(root)
    frequencies = Counter(text)
    print_huffman_tree(root)
    print("Symbol / 字符 | Frequency / 频率 | Code / 编码")
    for symbol in sorted(frequencies):
        print(f"{symbol!r:>6} | {frequencies[symbol]:>2} | {codes[symbol]}")
    bit_count = sum(frequencies[symbol] * len(codes[symbol]) for symbol in codes)
    assert sum(frequencies.values()) == 14 and bit_count == 43
    print(f"Encoded length / 编码总长度: {bit_count} bits")
    print("Ties may change codes but not the optimal length / 同频率编码不唯一。")

    for answer in THEORY_ANSWERS.values():
        print(answer)

    print("Problem 6 / 第 6 题: minimum unit intervals")
    points = [0, 0.5, 1, 1.5, 2.5, 4]
    intervals = minimum_unit_intervals(points)
    assert intervals == [(0, 1), (1.5, 2.5), (4, 5)]
    print(f"Points / 点: {points}")
    labels = ", ".join(f"[{start}, {end}]" for start, end in intervals)
    print(f"Intervals / 区间: {labels}; count / 数量: {len(intervals)}")

    print("\nProblem 7 / 第 7 题: minimum weighted completion time")
    jobs = [Job("A", 3, 1), Job("B", 1, 2), Job("C", 2, 3)]
    schedule = optimal_job_schedule(jobs)
    total = weighted_completion_time(schedule)
    assert [job.name for job in schedule] == ["B", "C", "A"] and total == 17
    elapsed = 0
    for job in schedule:
        elapsed += job.processing_time
        print(f"{job.name}: t={job.processing_time}, w={job.weight}, "
              f"C={elapsed}, w*C={job.weight * elapsed}")
    print(f"Total / 加权总和: {total}")

    print("\nProblem 8 / 第 8 题: minimum flower cost")
    total, purchases = minimum_flower_cost([2, 5, 6, 3, 8], 2)
    assert total == 36
    for friend, price, multiplier in purchases:
        print(f"Friend / 朋友 {friend}: {price} x {multiplier} = {price * multiplier}")
    print(f"Minimum total / 最低总价: {total}")
    print("\nAll example checks passed / 示例断言全部通过。")


if __name__ == "__main__":
    main()
