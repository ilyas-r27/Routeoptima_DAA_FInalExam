"""
RouteOptima CLI Demo — Smart Delivery Routing.

Generates a city road network and finds the shortest delivery route
using both Dijkstra and Bellman-Ford, then compares results.
"""

from __future__ import annotations
import argparse
import random
import time

from src.graph import Graph
from src.generator import generate_road_network
from src.dijkstra import dijkstra, reconstruct_path as dijkstra_path
from src.bellman_ford import bellman_ford, reconstruct_path as bf_path


def format_path(path: list, max_display: int = 15) -> str:
    """Format a path for display, truncating if too long."""
    if path is None:
        return "(unreachable)"
    if len(path) <= max_display:
        return " -> ".join(str(v) for v in path)
    head = " -> ".join(str(v) for v in path[:5])
    tail = " -> ".join(str(v) for v in path[-3:])
    return f"{head} -> ... ({len(path)-8} hops) ... -> {tail}"


def run_demo(num_vertices: int, seed: int, source: int, target: int):
    """Run the full demo: generate graph, solve with both algorithms, compare."""
    print("=" * 65)
    print("  RouteOptima — Smart Delivery Routing Demo")
    print("=" * 65)

    # Generate road network
    print(f"\n[1] Generating road network: V={num_vertices}, seed={seed}")
    graph = generate_road_network(num_vertices, density_factor=3.0, seed=seed)
    print(f"    Created: {graph}")

    # Validate source and target
    source = source % num_vertices
    target = target % num_vertices
    if source == target:
        target = (source + 1) % num_vertices
    print(f"    Route: Location {source} → Location {target}")

    # --- Dijkstra ---
    print(f"\n[2] Running Dijkstra's Algorithm (binary min-heap)...")
    t0 = time.perf_counter()
    dist_d, parent_d = dijkstra(graph, source)
    t_dijkstra = (time.perf_counter() - t0) * 1000
    path_d = dijkstra_path(parent_d, source, target)
    print(f"    Shortest distance : {dist_d[target]:.2f}")
    print(f"    Path              : {format_path(path_d)}")
    print(f"    Time              : {t_dijkstra:.3f} ms")

    # --- Bellman-Ford ---
    print(f"\n[3] Running Bellman-Ford Algorithm...")
    t0 = time.perf_counter()
    dist_bf, parent_bf, neg_cycle = bellman_ford(graph, source)
    t_bellman = (time.perf_counter() - t0) * 1000
    path_bf = bf_path(parent_bf, source, target)
    print(f"    Shortest distance : {dist_bf[target]:.2f}")
    print(f"    Path              : {format_path(path_bf)}")
    print(f"    Negative cycle    : {'YES' if neg_cycle else 'No'}")
    print(f"    Time              : {t_bellman:.3f} ms")

    # --- Cross-check ---
    print(f"\n[4] Cross-check")
    match = abs(dist_d[target] - dist_bf[target]) < 1e-9
    print(f"    Distances match   : {'YES ✓' if match else 'NO ✗'}")
    if t_bellman > 0:
        speedup = t_bellman / t_dijkstra if t_dijkstra > 0 else float("inf")
        print(f"    Dijkstra speedup  : {speedup:.1f}x faster")

    # Full agreement check on all vertices
    all_match = all(
        abs(dist_d[v] - dist_bf[v]) < 1e-9 for v in range(num_vertices)
    )
    print(f"    All {num_vertices} distances agree: {'YES ✓' if all_match else 'NO ✗'}")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(
        description="RouteOptima — Smart Delivery Routing Demo"
    )
    parser.add_argument(
        "-n", "--vertices", type=int, default=1000,
        help="Number of locations/vertices (default: 1000)"
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--source", type=int, default=0,
        help="Source location ID (default: 0)"
    )
    parser.add_argument(
        "--target", type=int, default=None,
        help="Target location ID (default: last vertex)"
    )
    args = parser.parse_args()

    target = args.target if args.target is not None else args.vertices - 1
    run_demo(args.vertices, args.seed, args.source, target)


if __name__ == "__main__":
    main()
