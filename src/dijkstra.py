"""
Dijkstra's shortest-path algorithm using a binary min-heap.

Time complexity:  O((V + E) log V)
Space complexity: O(V + E)

Requires all edge weights to be non-negative.
"""

from __future__ import annotations
import heapq
from typing import Dict, List, Optional, Tuple

from src.graph import Graph

INF = float("inf")


def dijkstra(
    graph: Graph, source: int
) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Compute single-source shortest paths from `source` using Dijkstra's
    algorithm with a binary min-heap (via Python's heapq).

    Parameters
    ----------
    graph  : weighted directed Graph (non-negative weights)
    source : source vertex id

    Returns
    -------
    dist   : dict mapping vertex -> shortest distance from source
    parent : dict mapping vertex -> predecessor on shortest path (None for source)
    """
    V = graph.num_vertices

    dist: Dict[int, float] = {v: INF for v in range(V)}
    parent: Dict[int, Optional[int]] = {v: None for v in range(V)}
    visited = [False] * V

    dist[source] = 0.0
    # Min-heap entries: (distance, vertex)
    pq: List[Tuple[float, int]] = [(0.0, source)]

    while pq:
        d_u, u = heapq.heappop(pq)

        if visited[u]:
            continue  # stale heap entry
        visited[u] = True

        for v, w in graph.neighbors(u):
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, parent


def reconstruct_path(
    parent: Dict[int, Optional[int]], source: int, target: int
) -> Optional[List[int]]:
    """Reconstruct the shortest path from source to target using the parent map."""
    if parent[target] is None and target != source:
        return None  # unreachable

    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path
