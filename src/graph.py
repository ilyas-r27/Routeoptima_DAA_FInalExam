"""
Graph data structure for RouteOptima.

Uses an adjacency list for Dijkstra (fast neighbor lookup)
and can export an edge list for Bellman-Ford.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Graph:
    """Weighted directed graph using adjacency list representation."""

    num_vertices: int
    adjacency: Dict[int, List[Tuple[int, float]]] = field(default_factory=dict)

    def __post_init__(self):
        for v in range(self.num_vertices):
            if v not in self.adjacency:
                self.adjacency[v] = []

    def add_edge(self, u: int, v: int, weight: float) -> None:
        """Add a directed edge u -> v with the given weight."""
        self.adjacency[u].append((v, weight))

    def add_undirected_edge(self, u: int, v: int, weight: float) -> None:
        """Add an undirected edge (both directions) with the given weight."""
        self.adjacency[u].append((v, weight))
        self.adjacency[v].append((u, weight))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        """Return list of (neighbor, weight) pairs for vertex u."""
        return self.adjacency[u]

    def edge_list(self) -> List[Tuple[int, int, float]]:
        """Return all edges as (u, v, weight) triples (for Bellman-Ford)."""
        edges = []
        for u in range(self.num_vertices):
            for v, w in self.adjacency[u]:
                edges.append((u, v, w))
        return edges

    def num_edges(self) -> int:
        """Count total directed edges."""
        return sum(len(adj) for adj in self.adjacency.values())

    def __repr__(self) -> str:
        return f"Graph(V={self.num_vertices}, E={self.num_edges()})"
