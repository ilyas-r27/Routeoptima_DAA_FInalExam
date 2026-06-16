"""
Plotting script for RouteOptima benchmark results.

Reads bench/results.csv and generates:
  1. Runtime vs Input Size (log-log) plot
  2. Speedup vs Input Size plot

Output: bench/runtime_plot.png, bench/speedup_plot.png
"""

from __future__ import annotations
import csv
import os
import sys

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use("Agg")  # non-interactive backend


def load_results(path: str = "bench/results.csv") -> dict:
    """Load benchmark CSV into column-oriented dict."""
    data = {"V": [], "E": [], "dijkstra_avg_ms": [], "bellman_ford_avg_ms": [], "speedup": []}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data["V"].append(int(row["V"]))
            data["E"].append(int(row["E"]))
            data["dijkstra_avg_ms"].append(float(row["dijkstra_avg_ms"]))
            data["bellman_ford_avg_ms"].append(float(row["bellman_ford_avg_ms"]))
            data["speedup"].append(float(row["speedup"]))
    return data


def plot_runtime(data: dict, output_dir: str = "bench"):
    """Generate a log-log runtime comparison plot."""
    fig, ax = plt.subplots(figsize=(10, 6))

    V = data["V"]
    ax.plot(V, data["dijkstra_avg_ms"], "o-", color="#2196F3", linewidth=2,
            markersize=8, label="Dijkstra (binary heap)")
    ax.plot(V, data["bellman_ford_avg_ms"], "s-", color="#F44336", linewidth=2,
            markersize=8, label="Bellman-Ford")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Number of Vertices (V)", fontsize=13)
    ax.set_ylabel("Average Runtime (ms)", fontsize=13)
    ax.set_title("RouteOptima: Dijkstra vs Bellman-Ford — Runtime Comparison", fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(True, which="both", alpha=0.3)
    ax.tick_params(labelsize=11)

    plt.tight_layout()
    path = os.path.join(output_dir, "runtime_plot.png")
    fig.savefig(path, dpi=150)
    print(f"  Saved: {path}")
    plt.close(fig)


def plot_speedup(data: dict, output_dir: str = "bench"):
    """Generate a speedup bar/line chart."""
    fig, ax = plt.subplots(figsize=(10, 5))

    V = data["V"]
    ax.bar([str(v) for v in V], data["speedup"], color="#4CAF50", alpha=0.8, edgecolor="#388E3C")

    ax.set_xlabel("Number of Vertices (V)", fontsize=13)
    ax.set_ylabel("Speedup (Bellman-Ford time / Dijkstra time)", fontsize=13)
    ax.set_title("RouteOptima: Dijkstra Speedup over Bellman-Ford", fontsize=14)
    ax.grid(axis="y", alpha=0.3)
    ax.tick_params(labelsize=11)

    # Add value labels on bars
    for i, (v, s) in enumerate(zip(V, data["speedup"])):
        ax.text(i, s + 0.3, f"{s:.1f}x", ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(output_dir, "speedup_plot.png")
    fig.savefig(path, dpi=150)
    print(f"  Saved: {path}")
    plt.close(fig)


def plot_empirical_exponent(data: dict, output_dir: str = "bench"):
    """Estimate and plot empirical growth exponents using log-log regression."""
    fig, ax = plt.subplots(figsize=(10, 6))

    V = np.array(data["V"], dtype=float)
    log_V = np.log10(V)

    for label, key, color, marker in [
        ("Dijkstra", "dijkstra_avg_ms", "#2196F3", "o"),
        ("Bellman-Ford", "bellman_ford_avg_ms", "#F44336", "s"),
    ]:
        times = np.array(data[key], dtype=float)
        log_t = np.log10(times)

        # Linear regression on log-log data: log(t) = slope * log(V) + intercept
        coeffs = np.polyfit(log_V, log_t, 1)
        slope = coeffs[0]

        # Plot data and fitted line
        ax.scatter(log_V, log_t, color=color, marker=marker, s=60, zorder=5)
        fit_line = np.polyval(coeffs, log_V)
        ax.plot(log_V, fit_line, "--", color=color, linewidth=1.5,
                label=f"{label} (slope ≈ {slope:.2f})")

    ax.set_xlabel("log₁₀(V)", fontsize=13)
    ax.set_ylabel("log₁₀(Runtime in ms)", fontsize=13)
    ax.set_title("Empirical Growth Exponent (log-log regression)", fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    plt.tight_layout()
    path = os.path.join(output_dir, "exponent_plot.png")
    fig.savefig(path, dpi=150)
    print(f"  Saved: {path}")
    plt.close(fig)


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "bench/results.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Run the benchmark first.")
        sys.exit(1)

    output_dir = os.path.dirname(csv_path) or "bench"
    print(f"\nGenerating plots from {csv_path} ...")
    data = load_results(csv_path)
    plot_runtime(data, output_dir)
    plot_speedup(data, output_dir)
    plot_empirical_exponent(data, output_dir)
    print("Done!\n")


if __name__ == "__main__":
    main()
