"""COMP9123 Tutorial 8 - Graph programming solutions.

The module implements traversal helpers for Problems 1-2 and solutions for
Problems 4, 5, 7, 8, 9, 10 and 11. Problems 3 and 6 are proof questions.
Graphs are represented as adjacency dictionaries: {vertex: [neighbour, ...]}.
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Hashable, Iterable, List, Mapping, Optional, Set, Tuple, TypeVar


Vertex = TypeVar("Vertex", bound=Hashable)
Graph = Mapping[Vertex, Iterable[Vertex]]


# Problems 1 and 2
def bfs_layers(graph: Graph[Vertex], start: Vertex) -> List[List[Vertex]]:
    """Return BFS layers for the component reachable from ``start`` in O(n + m)."""
    visited = {start}
    queue: Deque[Vertex] = deque([start])
    layers: List[List[Vertex]] = []

    while queue:
        layer: List[Vertex] = []
        for _ in range(len(queue)):
            vertex = queue.popleft()
            layer.append(vertex)
            for neighbour in graph.get(vertex, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        layers.append(layer)
    return layers


def dfs_forest(graph: Graph[Vertex], start: Vertex) -> List[Vertex]:
    """Return DFS visit order, restarting in other components when necessary."""
    order: List[Vertex] = []
    visited: Set[Vertex] = set()
    vertices = [start] + [vertex for vertex in graph if vertex != start]

    def visit(vertex: Vertex) -> None:
        visited.add(vertex)
        order.append(vertex)
        for neighbour in graph.get(vertex, []):
            if neighbour not in visited:
                visit(neighbour)

    for vertex in vertices:
        if vertex not in visited:
            visit(vertex)
    return order


# Problem 4
def bipartition(graph: Graph[Vertex]) -> Optional[Tuple[Set[Vertex], Set[Vertex]]]:
    """Return two colour classes, or None when an odd cycle makes this impossible.

    BFS colours every edge's endpoints differently. A same-colour edge proves
    the graph is not bipartite. Restarting from uncoloured vertices handles a
    disconnected graph. Time complexity: O(n + m).
    """
    colour: Dict[Vertex, int] = {}
    for start in graph:
        if start in colour:
            continue
        colour[start] = 0
        queue: Deque[Vertex] = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbour in graph.get(vertex, []):
                if neighbour not in colour:
                    colour[neighbour] = 1 - colour[vertex]
                    queue.append(neighbour)
                elif colour[neighbour] == colour[vertex]:
                    return None
    return (
        {vertex for vertex, value in colour.items() if value == 0},
        {vertex for vertex, value in colour.items() if value == 1},
    )


# Problem 5
def find_undirected_cycle(graph: Graph[Vertex]) -> Optional[List[Vertex]]:
    """Return one undirected cycle as [v0, ..., v0], or None if acyclic.

    DFS records each vertex's parent. Encountering an already visited neighbour
    other than the parent is a back edge; following parent links reconstructs
    the cycle. Time complexity: O(n + m).
    """
    visited: Set[Vertex] = set()
    parent: Dict[Vertex, Optional[Vertex]] = {}

    def visit(vertex: Vertex, previous: Optional[Vertex]) -> Optional[List[Vertex]]:
        visited.add(vertex)
        parent[vertex] = previous
        for neighbour in graph.get(vertex, []):
            if neighbour == previous:
                continue
            if neighbour in visited:
                cycle = [vertex]
                current = vertex
                while current != neighbour:
                    ancestor = parent[current]
                    if ancestor is None:
                        break
                    cycle.append(ancestor)
                    current = ancestor
                if current == neighbour:
                    cycle.append(vertex)
                    return cycle
            else:
                cycle = visit(neighbour, vertex)
                if cycle is not None:
                    return cycle
        return None

    for start in graph:
        if start not in visited:
            cycle = visit(start, None)
            if cycle is not None:
                return cycle
    return None


# Problem 7
def get_stuck_vertex(matrix: List[List[bool]]) -> Optional[int]:
    """Return a directed get-stuck vertex in O(n) time, or None.

    Candidate elimination examines one matrix entry per competitor: if candidate
    has an outgoing edge to i, candidate cannot qualify; otherwise i lacks the
    required incoming edge from candidate. One O(n) verification remains.
    """
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square")
    if n == 0:
        return None

    candidate = 0
    for vertex in range(1, n):
        if matrix[candidate][vertex]:
            candidate = vertex

    for vertex in range(n):
        if vertex == candidate:
            continue
        if not matrix[vertex][candidate] or matrix[candidate][vertex]:
            return None
    return candidate


# Problem 8
def component_minimums(graph: Graph[int]) -> Dict[int, int]:
    """Map each vertex to the smallest-numbered vertex in its component.

    A DFS/BFS finds each component once, then assigns its minimum to every
    member. Time complexity: O(n + m).
    """
    result: Dict[int, int] = {}
    for start in graph:
        if start in result:
            continue
        component: List[int] = []
        queue: Deque[int] = deque([start])
        result[start] = start  # marks it discovered temporarily
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for neighbour in graph.get(vertex, []):
                if neighbour not in result:
                    result[neighbour] = neighbour
                    queue.append(neighbour)
        minimum = min(component)
        for vertex in component:
            result[vertex] = minimum
    return result


# Problems 9 and 10
def _low_link_values(graph: Graph[Vertex]) -> Tuple[List[Tuple[Vertex, Vertex]], Set[Vertex]]:
    """Tarjan DFS returning all bridges and articulation points in O(n + m)."""
    discovery: Dict[Vertex, int] = {}
    low: Dict[Vertex, int] = {}
    bridges: List[Tuple[Vertex, Vertex]] = []
    cut_vertices: Set[Vertex] = set()
    time = 0

    def visit(vertex: Vertex, previous: Optional[Vertex]) -> None:
        nonlocal time
        discovery[vertex] = low[vertex] = time
        time += 1
        children = 0

        for neighbour in graph.get(vertex, []):
            if neighbour == previous:
                continue
            if neighbour not in discovery:
                children += 1
                visit(neighbour, vertex)
                low[vertex] = min(low[vertex], low[neighbour])

                # No descendant of neighbour can reach vertex or an ancestor.
                if low[neighbour] > discovery[vertex]:
                    bridges.append((vertex, neighbour))
                if previous is not None and low[neighbour] >= discovery[vertex]:
                    cut_vertices.add(vertex)
            else:
                low[vertex] = min(low[vertex], discovery[neighbour])

        # A DFS root is a cut vertex only if it has multiple DFS children.
        if previous is None and children > 1:
            cut_vertices.add(vertex)

    for start in graph:
        if start not in discovery:
            visit(start, None)
    return bridges, cut_vertices


def find_bridges(graph: Graph[Vertex]) -> List[Tuple[Vertex, Vertex]]:
    """Return every cut edge (bridge) in an undirected graph in O(n + m)."""
    return _low_link_values(graph)[0]


def find_articulation_points(graph: Graph[Vertex]) -> Set[Vertex]:
    """Return every cut vertex in an undirected graph in O(n + m)."""
    return _low_link_values(graph)[1]


# Problem 11
def minimum_snakes_and_ladders_rolls(
    jumps: Mapping[int, int], board_size: int = 100
) -> Optional[int]:
    """Return the minimum dice rolls from square 1 to ``board_size`` using BFS.

    Each square is a vertex. A die result from 1 to 6 creates an edge to the
    resulting square after applying a snake or ladder. Since each edge costs one
    roll, BFS finds the minimum number of rolls.
    """
    if board_size < 1:
        raise ValueError("board_size must be positive")

    queue: Deque[Tuple[int, int]] = deque([(1, 0)])
    visited = {1}
    while queue:
        square, rolls = queue.popleft()
        if square == board_size:
            return rolls
        for die in range(1, 7):
            landing = square + die
            if landing > board_size:
                continue
            destination = jumps.get(landing, landing)
            if not 1 <= destination <= board_size:
                raise ValueError("jump destination is outside the board")
            if destination not in visited:
                visited.add(destination)
                queue.append((destination, rolls + 1))
    return None


if __name__ == "__main__":
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["B", "C"],
        "E": [],
    }
    assert bfs_layers(graph, "A") == [["A"], ["B", "C"], ["D"]]
    assert dfs_forest(graph, "A") == ["A", "B", "D", "C", "E"]
    assert bipartition(graph) is not None
    assert find_undirected_cycle(graph) is not None

    triangle = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    assert bipartition(triangle) is None
    assert component_minimums({1: [2], 2: [1], 3: [4], 4: [3]}) == {
        1: 1,
        2: 1,
        3: 3,
        4: 3,
    }

    matrix = [
        [False, True, True, True],
        [False, False, True, True],
        [False, False, False, True],
        [False, False, False, False],
    ]
    assert get_stuck_vertex(matrix) == 3

    bridge_graph = {1: [2], 2: [1, 3, 4], 3: [2, 4], 4: [2, 3, 5], 5: [4]}
    assert set(find_bridges(bridge_graph)) == {(1, 2), (4, 5)}
    assert find_articulation_points(bridge_graph) == {2, 4}
    assert minimum_snakes_and_ladders_rolls({2: 15}, board_size=20) == 2
    print("Tutorial 8 graph checks passed.")
