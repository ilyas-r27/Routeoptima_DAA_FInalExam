"""
Bellman-Ford single-source shortest-path algorithm.

Time complexity:  O(V * E)
Space complexity: O(V)

Handles negative edge weights and detects negative-weight cycles.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple

from src.graph import Graph

INF = float("inf")


def bellman_ford(
    graph: Graph, source: int
) -> Tuple[Dict[int, float], Dict[int, Optional[int]], bool]:
    """
    Compute single-source shortest paths from `source` using the
    Bellman-Ford algorithm.

    Parameters
    ----------
    graph  : weighted directed Graph
    source : source vertex id

    Returns
    -------
    dist              : dict mapping vertex -> shortest distance from source
    parent            : dict mapping vertex -> predecessor on shortest path
    has_negative_cycle : True if a negative-weight cycle is reachable from source
    """
    V = graph.num_vertices
    edges = graph.edge_list()

    dist: Dict[int, float] = {v: INF for v in range(V)}
    parent: Dict[int, Optional[int]] = {v: None for v in range(V)}
    dist[source] = 0.0

    # Relaxation: repeat V-1 times
    for i in range(V - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        # Early termination: if no update occurred, we are done
        if not updated:
            break

    # Negative-cycle detection: one more pass
    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, parent, has_negative_cycle


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
