"""COMP9123 Tutorial 13 - Exam revision programming solutions.

This file implements the programming-friendly algorithms from Problems 3-8.
Each public function has a short correctness/complexity note in its docstring,
and the ``__main__`` block provides small executable checks.
"""

from __future__ import annotations

from collections import Counter, deque
import heapq
import math
from dataclasses import dataclass
from typing import Iterable, Optional, Sequence


# Problem 3
def new_sort(values: list[int]) -> None:
    """Sort ``values`` in place using the three-call overlapping recursion.

    The first and third calls sort the first 2n/3 values; the middle call sorts
    the last 2n/3 values.  This is the classic *stooge sort* pattern.  After
    the first two calls, the largest values have moved to the final third; the
    last call therefore finishes sorting the first two thirds.  The recurrence
    is T(n) = 3T(2n/3) + O(1), hence T(n) = O(n**log_(3/2)(3)).
    """

    def sort_range(first: int, last: int) -> None:
        length = last - first + 1
        if length <= 1:
            return
        if values[first] > values[last]:
            values[first], values[last] = values[last], values[first]
        if length > 2:
            third = length // 3
            sort_range(first, last - third)
            sort_range(first + third, last)
            sort_range(first, last - third)

    if values:
        sort_range(0, len(values) - 1)


# Problem 4
def find_local_minimum(values: Sequence[int]) -> int:
    """Return an index whose value is smaller than its existing neighbours.

    Values must be distinct.  If the midpoint is not locally minimal, moving
    towards a smaller neighbour preserves the existence of a local minimum,
    including at an endpoint.  Therefore one half is discarded per iteration:
    O(log n) time and O(1) auxiliary space.
    """
    if not values:
        raise ValueError("values must not be empty")
    if len(set(values)) != len(values):
        raise ValueError("values must be distinct")

    left, right = 0, len(values) - 1
    while left <= right:
        middle = (left + right) // 2
        smaller_than_left = middle == 0 or values[middle] < values[middle - 1]
        smaller_than_right = middle == len(values) - 1 or values[middle] < values[middle + 1]
        if smaller_than_left and smaller_than_right:
            return middle
        if middle > 0 and values[middle - 1] < values[middle]:
            right = middle - 1
        else:
            left = middle + 1
    raise RuntimeError("a local minimum must exist for distinct values")


# Problem 5
@dataclass
class BinaryTreeNode:
    """Minimal binary-tree node used by ``tree_diameter``."""

    value: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None


def tree_diameter(root: Optional[BinaryTreeNode]) -> int:
    """Return the longest simple-path length (number of edges) in a tree.

    A post-order traversal obtains both child heights.  The best path through a
    node has ``left_height + right_height`` edges, so inspecting every node
    once finds the global maximum in O(n) time and O(h) recursion stack space.
    """
    longest = 0

    def height(node: Optional[BinaryTreeNode]) -> int:
        nonlocal longest
        if node is None:
            return 0
        left_height = height(node.left)
        right_height = height(node.right)
        longest = max(longest, left_height + right_height)
        return 1 + max(left_height, right_height)

    height(root)
    return longest


# Problem 6
STAMP_VALUES = (64, 16, 4, 1)


def greedy_stamps(cents: int) -> Counter[int]:
    """Return the minimum-cardinality multiset for 1c, 4c, 16c and 64c stamps.

    Repeatedly taking the largest denomination is optimal because every larger
    stamp equals four of the next denomination.  Replacing four smaller stamps
    with one larger stamp always reduces the count.  There are O(log_4 n)
    denominations to examine and the returned Counter uses O(log n) space.
    """
    if cents < 0:
        raise ValueError("cents must be non-negative")
    result: Counter[int] = Counter()
    remaining = cents
    for stamp in STAMP_VALUES:
        count, remaining = divmod(remaining, stamp)
        if count:
            result[stamp] = count
    return result


# Problem 7
def minimum_vertex_cover_tree(vertex_count: int, edges: Iterable[tuple[int, int]]) -> set[int]:
    """Return a minimum vertex cover of an undirected tree.

    The greedy rule is: choose the parent of any current leaf, then remove that
    parent and all incident edges.  Any cover must cover the leaf edge, and its
    parent covers every edge that selecting the leaf could cover, so the greedy
    choice is safe.  Queue-based degree updates visit each edge O(1) times:
    O(V + E) time and O(V + E) space.
    """
    if vertex_count < 0:
        raise ValueError("vertex_count must be non-negative")
    adjacency = [[] for _ in range(vertex_count)]
    edge_count = 0
    for u, v in edges:
        if not (0 <= u < vertex_count and 0 <= v < vertex_count) or u == v:
            raise ValueError("edges must join two different valid vertices")
        adjacency[u].append(v)
        adjacency[v].append(u)
        edge_count += 1
    if vertex_count and edge_count != vertex_count - 1:
        raise ValueError("input must be a tree")

    degree = [len(neighbours) for neighbours in adjacency]
    active = [True] * vertex_count
    leaves = deque(index for index, value in enumerate(degree) if value == 1)
    cover: set[int] = set()

    while leaves:
        leaf = leaves.popleft()
        if not active[leaf] or degree[leaf] != 1:
            continue
        parent = next(neighbour for neighbour in adjacency[leaf] if active[neighbour])
        cover.add(parent)
        active[parent] = False
        for neighbour in adjacency[parent]:
            if active[neighbour]:
                degree[neighbour] -= 1
                if degree[neighbour] == 1:
                    leaves.append(neighbour)
        degree[parent] = 0
    return cover


# Problem 8
def minimum_shopping_time(
    node_count: int,
    roads: Iterable[tuple[int, int, int]],
    items_at_node: Sequence[int],
    item_type_count: int,
) -> float:
    """Return the minimum finishing time for two shoppers to collect all items.

    Nodes and roads use zero-based indices.  A Dijkstra state ``(node, mask)``
    records the shortest time to reach a node while owning the item set ``mask``.
    At the destination, each shopper may use a different mask; their masks must
    union to all item types and the objective is the slower arrival time.

    Expanded-state Dijkstra costs O((N + M) 2**K log(N 2**K)).  A subset-DP
    pass combines destination masks in O(K 2**K), avoiding a quadratic scan of
    all mask pairs.
    """
    if node_count <= 0 or len(items_at_node) != node_count or item_type_count < 0:
        raise ValueError("invalid node or item configuration")
    if item_type_count > 20:
        raise ValueError("item_type_count is too large for bitmask state search")
    full_mask = (1 << item_type_count) - 1
    if any(mask < 0 or mask & ~full_mask for mask in items_at_node):
        raise ValueError("an item mask contains an unknown item type")

    graph = [[] for _ in range(node_count)]
    for u, v, weight in roads:
        if not (0 <= u < node_count and 0 <= v < node_count) or weight <= 0:
            raise ValueError("roads must have valid endpoints and positive weights")
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    mask_count = 1 << item_type_count
    distance = [[math.inf] * mask_count for _ in range(node_count)]
    start_mask = items_at_node[0]
    distance[0][start_mask] = 0
    heap: list[tuple[int, int, int]] = [(0, 0, start_mask)]
    while heap:
        current_time, node, mask = heapq.heappop(heap)
        if current_time != distance[node][mask]:
            continue
        for neighbour, weight in graph[node]:
            next_mask = mask | items_at_node[neighbour]
            next_time = current_time + weight
            if next_time < distance[neighbour][next_mask]:
                distance[neighbour][next_mask] = next_time
                heapq.heappush(heap, (next_time, neighbour, next_mask))

    best_superset = distance[node_count - 1][:]
    for bit in range(item_type_count):
        for mask in range(mask_count):
            if not mask & (1 << bit):
                best_superset[mask] = min(best_superset[mask], best_superset[mask | (1 << bit)])
    return min(max(distance[-1][mask], best_superset[full_mask ^ mask]) for mask in range(mask_count))


if __name__ == "__main__":
    numbers = [4, 2, 5, 1, 3]
    new_sort(numbers)
    assert numbers == [1, 2, 3, 4, 5]

    local_index = find_local_minimum([9, 6, 7, 3, 5, 8])
    assert local_index in {1, 3}

    tree = BinaryTreeNode(1, BinaryTreeNode(2, BinaryTreeNode(4), BinaryTreeNode(5)), BinaryTreeNode(3))
    assert tree_diameter(tree) == 3

    stamps = greedy_stamps(85)
    assert stamps == Counter({64: 1, 16: 1, 4: 1, 1: 1})

    cover = minimum_vertex_cover_tree(5, [(0, 1), (1, 2), (1, 3), (3, 4)])
    assert cover == {1, 3}

    roads_example = [(0, 1, 3), (0, 2, 4), (1, 3, 5), (2, 3, 2)]
    # Node item masks: node 0 has item 0, node 1 has item 1, node 2 has item 2.
    assert minimum_shopping_time(4, roads_example, [1, 2, 4, 0], 3) == 8
    print("Tutorial 13 revision checks passed.")
