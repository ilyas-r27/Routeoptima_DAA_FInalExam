"""
Random weighted graph generator for benchmarking.

Generates connected graphs that simulate road networks:
- Ensures connectivity via a random spanning tree first
- Adds extra edges to reach the desired density
- Weights represent distances (positive floats)
"""

from __future__ import annotations
import random
from typing import Optional

from src.graph import Graph


def generate_connected_graph(
    num_vertices: int,
    num_edges: int,
    weight_range: tuple = (1.0, 100.0),
    seed: Optional[int] = None,
    directed: bool = False,
) -> Graph:
    """
    Generate a connected weighted graph.

    1. Build a random spanning tree (V-1 edges) to guarantee connectivity.
    2. Add random edges until the target edge count is reached.

    Parameters
    ----------
    num_vertices : number of vertices (V)
    num_edges    : target number of undirected edges (must be >= V-1)
    weight_range : (min_weight, max_weight) for uniform random weights
    seed         : random seed for reproducibility
    directed     : if True, generate a directed graph (each undirected edge
                   becomes two directed edges for the spanning tree,
                   extra edges are single-direction)

    Returns
    -------
    A connected Graph instance.
    """
    if seed is not None:
        random.seed(seed)

    V = num_vertices
    min_edges = V - 1
    if num_edges < min_edges:
        raise ValueError(f"Need at least {min_edges} edges for {V} vertices")

    graph = Graph(num_vertices=V)
    edge_set = set()
    w_lo, w_hi = weight_range

    # Step 1: Random spanning tree via random permutation
    vertices = list(range(V))
    random.shuffle(vertices)
    for i in range(1, V):
        u, v = vertices[i - 1], vertices[i]
        w = round(random.uniform(w_lo, w_hi), 2)
        if directed:
            graph.add_edge(u, v, w)
            graph.add_edge(v, u, w)
        else:
            graph.add_undirected_edge(u, v, w)
        edge_set.add((min(u, v), max(u, v)))

    # Step 2: Add extra random edges
    extra_needed = num_edges - min_edges
    attempts = 0
    max_attempts = extra_needed * 20  # avoid infinite loop on dense graphs

    while len(edge_set) - min_edges < extra_needed and attempts < max_attempts:
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        if u == v:
            attempts += 1
            continue
        key = (min(u, v), max(u, v))
        if key in edge_set:
            attempts += 1
            continue
        w = round(random.uniform(w_lo, w_hi), 2)
        if directed:
            graph.add_edge(u, v, w)
        else:
            graph.add_undirected_edge(u, v, w)
        edge_set.add(key)
        attempts += 1

    return graph


def generate_road_network(
    num_vertices: int,
    density_factor: float = 3.0,
    seed: Optional[int] = None,
) -> Graph:
    """
    Convenience function: generate a road-network-like graph.

    density_factor controls E/V ratio (typical roads: 2-4 edges per vertex).
    E.g., density_factor=3 → approximately 3*V edges.
    """
    num_edges = int(num_vertices * density_factor)
    # Cap at max possible undirected edges
    max_edges = num_vertices * (num_vertices - 1) // 2
    num_edges = min(num_edges, max_edges)

    return generate_connected_graph(
        num_vertices=num_vertices,
        num_edges=num_edges,
        weight_range=(1.0, 100.0),
        seed=seed,
        directed=False,
    )
