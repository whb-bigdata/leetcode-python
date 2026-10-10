"""COMP9123 Tutorial 9 - Graph algorithm programming solutions.

Problem 3 is a proof/counterexample question. The remaining algorithmic
questions are implemented below using adjacency lists and weighted edge lists.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from math import inf
from typing import DefaultDict, Dict, Hashable, Iterable, List, Mapping, Optional, Sequence, Set, Tuple, TypeVar


Vertex = TypeVar("Vertex", bound=Hashable)
WeightedEdge = Tuple[Vertex, Vertex, float]
WeightedGraph = Mapping[Vertex, Iterable[Tuple[Vertex, float]]]


# Problem 1: Dijkstra needs no conceptual change for directed graphs.  Simply
# relax outgoing edges only; do not add a reversed copy of each edge.
def dijkstra(graph: WeightedGraph[Vertex], source: Vertex) -> Tuple[Dict[Vertex, float], Dict[Vertex, Optional[Vertex]]]:
    """Compute directed non-negative shortest paths from source in O(m log n)."""
    distances: Dict[Vertex, float] = {vertex: inf for vertex in graph}
    distances[source] = 0
    parents: Dict[Vertex, Optional[Vertex]] = {source: None}
    serial = count()
    queue: List[Tuple[float, int, Vertex]] = [(0, next(serial), source)]

    while queue:
        distance, _, vertex = heappop(queue)
        if distance != distances.get(vertex, inf):
            continue
        for neighbour, weight in graph.get(vertex, []):
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            candidate = distance + weight
            if candidate < distances.get(neighbour, inf):
                distances[neighbour] = candidate
                parents[neighbour] = vertex
                heappush(queue, (candidate, next(serial), neighbour))
    return distances, parents


def reconstruct_path(parents: Mapping[Vertex, Optional[Vertex]], target: Vertex) -> Optional[List[Vertex]]:
    """Reconstruct a source-to-target path from a Dijkstra parent map."""
    if target not in parents:
        return None
    path: List[Vertex] = []
    current: Optional[Vertex] = target
    while current is not None:
        path.append(current)
        current = parents[current]
    return list(reversed(path))


class _DisjointSet:
    """Union-Find with path compression and union by size."""

    def __init__(self, vertices: Iterable[Vertex]) -> None:
        self.parent = {vertex: vertex for vertex in vertices}
        self.size = {vertex: 1 for vertex in self.parent}

    def find(self, vertex: Vertex) -> Vertex:
        while self.parent[vertex] != vertex:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def union(self, first: Vertex, second: Vertex) -> bool:
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root == second_root:
            return False
        if self.size[first_root] < self.size[second_root]:
            first_root, second_root = second_root, first_root
        self.parent[second_root] = first_root
        self.size[first_root] += self.size[second_root]
        return True


# Problem 2
def kruskal_mst(vertices: Iterable[Vertex], edges: Iterable[WeightedEdge[Vertex]]) -> List[WeightedEdge[Vertex]]:
    """Return an MST edge list in Kruskal insertion order."""
    vertex_list = list(vertices)
    disjoint_set = _DisjointSet(vertex_list)
    tree: List[WeightedEdge[Vertex]] = []
    for edge in sorted(edges, key=lambda item: item[2]):
        first, second, _ = edge
        if disjoint_set.union(first, second):
            tree.append(edge)
            if len(tree) == len(vertex_list) - 1:
                break
    if len(tree) != max(0, len(vertex_list) - 1):
        raise ValueError("graph is disconnected; an MST does not exist")
    return tree


def prim_mst(graph: WeightedGraph[Vertex], start: Vertex) -> List[WeightedEdge[Vertex]]:
    """Return an MST edge list in Prim insertion order, starting at start."""
    visited = {start}
    serial = count()
    queue: List[Tuple[float, int, Vertex, Vertex]] = []
    for neighbour, weight in graph.get(start, []):
        heappush(queue, (weight, next(serial), start, neighbour))

    tree: List[WeightedEdge[Vertex]] = []
    while queue:
        weight, _, first, second = heappop(queue)
        if second in visited:
            continue
        visited.add(second)
        tree.append((first, second, weight))
        for neighbour, next_weight in graph.get(second, []):
            if neighbour not in visited:
                heappush(queue, (next_weight, next(serial), second, neighbour))

    if len(visited) != len(graph):
        raise ValueError("graph is disconnected; an MST does not exist")
    return tree


def tutorial_problem_2() -> Tuple[List[WeightedEdge[str]], List[WeightedEdge[str]]]:
    """Compute Kruskal and Prim orders for Tutorial 9's displayed graph."""
    edges: List[WeightedEdge[str]] = [
        ("a", "b", 10), ("b", "c", 7), ("a", "d", 1), ("d", "e", 4),
        ("e", "f", 3), ("c", "f", 2), ("a", "e", 6), ("e", "c", 5),
    ]
    graph: DefaultDict[str, List[Tuple[str, float]]] = defaultdict(list)
    for first, second, weight in edges:
        graph[first].append((second, weight))
        graph[second].append((first, weight))
    return kruskal_mst(graph, edges), prim_mst(graph, "a")


# Problem 4
def shortest_path_fewest_edges(
    graph: WeightedGraph[Vertex], source: Vertex, target: Vertex
) -> Optional[List[Vertex]]:
    """Return a shortest path that uses the fewest edges among tied paths.

    For n vertices, every positive-length shortest path is simple and has at
    most n - 1 edges. Choosing M = n therefore makes one extra original length
    outweigh any possible difference in edge count. Dijkstra uses M*l(e) + 1.
    """
    vertex_count = len(graph)
    if vertex_count == 0:
        return None
    transformed = {
        vertex: [(neighbour, vertex_count * length + 1) for neighbour, length in edges]
        for vertex, edges in graph.items()
    }
    _, parents = dijkstra(transformed, source)
    return reconstruct_path(parents, target)


# Problem 5
def minimum_vertex_and_edge_cost_path(
    graph: WeightedGraph[Vertex], vertex_costs: Mapping[Vertex, float], source: Vertex, target: Vertex
) -> Tuple[float, Optional[List[Vertex]]]:
    """Find a minimum-cost path when both vertices and edges have positive costs.

    Pay c(source) initially. Transform each edge (u, v) to length l(u, v)+c(v),
    then use Dijkstra. This gives exactly sum(c(vertices)) + sum(l(edges)).
    """
    if source not in vertex_costs or target not in vertex_costs:
        raise ValueError("source and target must have vertex costs")
    transformed = {
        vertex: [(neighbour, length + vertex_costs[neighbour]) for neighbour, length in edges]
        for vertex, edges in graph.items()
    }
    distances, parents = dijkstra(transformed, source)
    if distances.get(target, inf) == inf:
        return inf, None
    return vertex_costs[source] + distances[target], reconstruct_path(parents, target)


def _tree_path_edges(tree: Sequence[WeightedEdge[Vertex]], source: Vertex, target: Vertex) -> List[WeightedEdge[Vertex]]:
    """Find the unique source-target path in a tree."""
    adjacency: DefaultDict[Vertex, List[WeightedEdge[Vertex]]] = defaultdict(list)
    for first, second, weight in tree:
        adjacency[first].append((first, second, weight))
        adjacency[second].append((second, first, weight))
    queue: Deque[Vertex] = deque([source])
    parent: Dict[Vertex, Optional[Tuple[Vertex, WeightedEdge[Vertex]]]] = {source: None}
    while queue:
        vertex = queue.popleft()
        if vertex == target:
            break
        for _, neighbour, weight in adjacency[vertex]:
            if neighbour not in parent:
                parent[neighbour] = (vertex, (vertex, neighbour, weight))
                queue.append(neighbour)
    if target not in parent:
        raise ValueError("tree does not connect both endpoints")
    path: List[WeightedEdge[Vertex]] = []
    current = target
    while parent[current] is not None:
        previous, edge = parent[current]
        path.append(edge)
        current = previous
    return path


# Problem 6
def improving_mst(vertices: Iterable[Vertex], edges: Iterable[WeightedEdge[Vertex]]) -> List[WeightedEdge[Vertex]]:
    """Implement the improving-MST algorithm with an arbitrary initial tree.

    Start with a DFS spanning tree. For each non-tree edge, add it conceptually,
    find its unique cycle, and remove the cycle's heaviest edge. With distinct
    weights this returns an MST; this direct implementation is O(mn).
    """
    vertex_list = list(vertices)
    edge_list = list(edges)
    if not vertex_list:
        return []

    disjoint_set = _DisjointSet(vertex_list)
    tree: List[WeightedEdge[Vertex]] = []
    non_tree: List[WeightedEdge[Vertex]] = []
    for edge in edge_list:
        first, second, _ = edge
        if disjoint_set.union(first, second):
            tree.append(edge)
        else:
            non_tree.append(edge)
    if len(tree) != len(vertex_list) - 1:
        raise ValueError("graph is disconnected; no spanning tree exists")

    for edge in non_tree:
        first, second, _ = edge
        cycle = _tree_path_edges(tree, first, second) + [edge]
        heaviest = max(cycle, key=lambda item: item[2])
        if heaviest != edge:
            tree.remove(heaviest)
            tree.append(edge)
    return tree


def _is_connected(vertices: Iterable[Vertex], edges: Iterable[WeightedEdge[Vertex]]) -> bool:
    vertex_list = list(vertices)
    if not vertex_list:
        return True
    adjacency: DefaultDict[Vertex, List[Vertex]] = defaultdict(list)
    for first, second, _ in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    visited = {vertex_list[0]}
    queue: Deque[Vertex] = deque([vertex_list[0]])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return len(visited) == len(vertex_list)


# Problem 7
def reverse_mst(vertices: Iterable[Vertex], edges: Iterable[WeightedEdge[Vertex]]) -> List[WeightedEdge[Vertex]]:
    """Implement reverse-delete MST by removing safe heavy edges.

    This literal version checks connectivity after each possible removal, giving
    O(m(n+m)) time with BFS/DFS connectivity checks.
    """
    vertex_list = list(vertices)
    tree = list(edges)
    for edge in sorted(list(edges), key=lambda item: item[2], reverse=True):
        candidate = list(tree)
        candidate.remove(edge)
        if _is_connected(vertex_list, candidate):
            tree = candidate
    return tree


# Problem 8
def maximum_bandwidth_matrix(vertices: Sequence[Vertex], edges: Iterable[WeightedEdge[Vertex]]) -> List[List[float]]:
    """Compute all-pairs maximum bottleneck bandwidth in O(n^3) time.

    This is Floyd-Warshall with max/min replacing min/add:
    B[i][j] = max(B[i][j], min(B[i][k], B[k][j])).
    The diagonal is infinity because an empty path has no limiting edge.
    """
    index = {vertex: position for position, vertex in enumerate(vertices)}
    size = len(vertices)
    bandwidth = [[0.0] * size for _ in range(size)]
    for position in range(size):
        bandwidth[position][position] = inf
    for first, second, value in edges:
        first_index, second_index = index[first], index[second]
        bandwidth[first_index][second_index] = max(bandwidth[first_index][second_index], value)
        bandwidth[second_index][first_index] = max(bandwidth[second_index][first_index], value)

    for middle in range(size):
        for first in range(size):
            for second in range(size):
                bandwidth[first][second] = max(
                    bandwidth[first][second],
                    min(bandwidth[first][middle], bandwidth[middle][second]),
                )
    return bandwidth


# Problem 9
@dataclass(frozen=True)
class LibraryRoadPlan:
    libraries: List[int]
    roads: List[Tuple[int, int]]
    total_cost: float


def minimum_library_road_plan(
    city_count: int,
    candidate_roads: Iterable[Tuple[int, int]],
    library_cost: float,
    road_cost: float,
) -> LibraryRoadPlan:
    """Return the minimum-cost library and road plan.

    If a road costs at least one library, build one library in every city.
    Otherwise, each connected component needs one library plus a DFS spanning
    tree of roads. This costs c_lib + (component_size - 1) * c_road per
    component and is optimal because each road is cheaper than a library.
    """
    if city_count < 0 or library_cost < 0 or road_cost < 0:
        raise ValueError("counts and costs must be non-negative")
    if road_cost >= library_cost:
        return LibraryRoadPlan(list(range(1, city_count + 1)), [], city_count * library_cost)

    adjacency: DefaultDict[int, List[int]] = defaultdict(list)
    for first, second in candidate_roads:
        if not 1 <= first <= city_count or not 1 <= second <= city_count:
            raise ValueError("road endpoint is outside the city range")
        adjacency[first].append(second)
        adjacency[second].append(first)

    libraries: List[int] = []
    roads: List[Tuple[int, int]] = []
    visited: Set[int] = set()
    for city in range(1, city_count + 1):
        if city in visited:
            continue
        libraries.append(city)
        visited.add(city)
        queue: Deque[int] = deque([city])
        while queue:
            current = queue.popleft()
            for neighbour in adjacency[current]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    roads.append((current, neighbour))
                    queue.append(neighbour)
    return LibraryRoadPlan(libraries, roads, len(libraries) * library_cost + len(roads) * road_cost)


if __name__ == "__main__":
    kruskal_order, prim_order = tutorial_problem_2()
    assert [edge[2] for edge in kruskal_order] == [1, 2, 3, 4, 7]
    assert [edge[2] for edge in prim_order] == [1, 4, 3, 2, 7]

    directed_graph = {"s": [("a", 2), ("b", 1)], "a": [("t", 2)], "b": [("t", 5)], "t": []}
    distances, parents = dijkstra(directed_graph, "s")
    assert distances["t"] == 4 and reconstruct_path(parents, "t") == ["s", "a", "t"]

    tied_paths = {"s": [("a", 1), ("t", 2)], "a": [("t", 1)], "t": []}
    assert shortest_path_fewest_edges(tied_paths, "s", "t") == ["s", "t"]
    assert minimum_vertex_and_edge_cost_path(directed_graph, {"s": 1, "a": 2, "b": 1, "t": 3}, "s", "t") == (
        10,
        ["s", "a", "t"],
    )

    vertices = ["a", "b", "c", "d"]
    edges: List[WeightedEdge[str]] = [("a", "b", 1), ("b", "c", 2), ("c", "d", 3), ("a", "d", 10), ("a", "c", 8)]
    assert sum(edge[2] for edge in improving_mst(vertices, edges)) == 6
    assert sum(edge[2] for edge in reverse_mst(vertices, edges)) == 6

    matrix = maximum_bandwidth_matrix(["a", "b", "c"], [("a", "b", 5), ("b", "c", 3), ("a", "c", 2)])
    assert matrix[0][2] == 3
    plan = minimum_library_road_plan(4, [(1, 2), (2, 3)], library_cost=6, road_cost=1)
    assert plan == LibraryRoadPlan([1, 4], [(1, 2), (2, 3)], 14)
    print("Tutorial 9 graph algorithm checks passed.")
