"""
Benchmark harness for RouteOptima.

Runs Dijkstra and Bellman-Ford on graphs of increasing size,
measures runtime, verifies correctness cross-check, and writes
results to a CSV file.
"""

from __future__ import annotations
import csv
import os
import time
import argparse
from typing import List, Tuple

from src.graph import Graph
from src.generator import generate_road_network
from src.dijkstra import dijkstra
from src.bellman_ford import bellman_ford


# Input sizes spanning two orders of magnitude (100 -> 10,000)
DEFAULT_SIZES = [100, 250, 500, 1000, 2500, 5000, 10000]
NUM_RUNS = 5          # runs per size for averaging
DENSITY_FACTOR = 3.0  # E ≈ 3V (road-network-like)
SEED = 42


def benchmark_single(graph: Graph, source: int) -> Tuple[float, float, bool]:
    """
    Run both algorithms once and return (dijkstra_ms, bellman_ms, match).
    """
    # Dijkstra
    t0 = time.perf_counter()
    dist_d, _ = dijkstra(graph, source)
    t_dijkstra = (time.perf_counter() - t0) * 1000

    # Bellman-Ford
    t0 = time.perf_counter()
    dist_bf, _, _ = bellman_ford(graph, source)
    t_bellman = (time.perf_counter() - t0) * 1000

    # Cross-check: all distances must agree
    match = all(
        abs(dist_d[v] - dist_bf[v]) < 1e-9 for v in range(graph.num_vertices)
    )

    return t_dijkstra, t_bellman, match


def run_benchmark(
    sizes: List[int] = DEFAULT_SIZES,
    num_runs: int = NUM_RUNS,
    output_path: str = "bench/results.csv",
):
    """
    Run the full benchmark sweep and write results to CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("=" * 72)
    print("  RouteOptima Benchmark — Dijkstra vs Bellman-Ford")
    print(f"  Sizes: {sizes}")
    print(f"  Runs per size: {num_runs}, Density E≈{DENSITY_FACTOR}V, Seed={SEED}")
    print("=" * 72)

    results = []

    for V in sizes:
        E_approx = int(V * DENSITY_FACTOR)
        print(f"\n  V = {V:>6}, E ≈ {E_approx:>8} ...", end=" ", flush=True)

        graph = generate_road_network(V, density_factor=DENSITY_FACTOR, seed=SEED)
        E_actual = graph.num_edges()

        dijkstra_times = []
        bellman_times = []
        all_match = True

        for run in range(num_runs):
            source = run % V  # vary source slightly across runs
            td, tb, match = benchmark_single(graph, source)
            dijkstra_times.append(td)
            bellman_times.append(tb)
            if not match:
                all_match = False

        avg_d = sum(dijkstra_times) / num_runs
        avg_b = sum(bellman_times) / num_runs
        min_d = min(dijkstra_times)
        min_b = min(bellman_times)
        speedup = avg_b / avg_d if avg_d > 0 else float("inf")

        status = "✓" if all_match else "✗ MISMATCH"
        print(
            f"Dijkstra: {avg_d:>10.2f} ms  |  "
            f"Bellman-Ford: {avg_b:>10.2f} ms  |  "
            f"Speedup: {speedup:>6.1f}x  |  {status}"
        )

        results.append({
            "V": V,
            "E": E_actual,
            "dijkstra_avg_ms": round(avg_d, 4),
            "dijkstra_min_ms": round(min_d, 4),
            "bellman_ford_avg_ms": round(avg_b, 4),
            "bellman_ford_min_ms": round(min_b, 4),
            "speedup": round(speedup, 2),
            "cross_check": "PASS" if all_match else "FAIL",
        })

    # Write CSV
    fieldnames = list(results[0].keys())
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n  Results saved to: {output_path}")
    print("=" * 72)

    return results


def main():
    parser = argparse.ArgumentParser(description="RouteOptima Benchmark")
    parser.add_argument(
        "--sizes", nargs="+", type=int, default=DEFAULT_SIZES,
        help="List of vertex counts to benchmark",
    )
    parser.add_argument(
        "--runs", type=int, default=NUM_RUNS,
        help="Number of runs per size (default: 5)",
    )
    parser.add_argument(
        "--output", type=str, default="bench/results.csv",
        help="Output CSV path (default: bench/results.csv)",
    )
    args = parser.parse_args()
    run_benchmark(sizes=args.sizes, num_runs=args.runs, output_path=args.output)


if __name__ == "__main__":
    main()
