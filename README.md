# RouteOptima - Smart Delivery Routing 

**EF234405 Design & Analysis of Algorithms - Final Exam (Group Capstone Project)**

RouteOptima models a city road network as a weighted undirected graph and finds the shortest delivery route between any two locations using two classic shortest-path algorithms:

- **Algorithm A — Dijkstra's Algorithm** (binary min-heap via `heapq`)
- **Algorithm B — Bellman-Ford Algorithm**

Both algorithms are implemented **from scratch** (no library shortest-path calls). The project benchmarks them across input sizes from 100 to 10,000 vertices, verifies correctness via cross-checking, and produces runtime comparison plots.

## Team

| Name | Student ID | Role |
|------|-----------|------|
| Muhammad Ilyas Rusdi | 5025241007 | Leader |
| Bismantaka Revano Dirgantara | 5025241075 | Member |


## Project Structure

```
routeoptima/
├── src/
│   ├── graph.py          # Graph data structure (adjacency list)
│   ├── dijkstra.py       # Dijkstra's algorithm (binary min-heap)
│   ├── bellman_ford.py   # Bellman-Ford algorithm
│   ├── generator.py      # Random connected graph generator
│   ├── demo.py           # CLI demo application
│   └── benchmark.py      # Benchmark harness (writes CSV)
├── plot.py               # Generates runtime & speedup plots
├── run_benchmark.sh      # One-command benchmark script
├── bench/                # Benchmark outputs (CSV + plots)
├── requirements.txt
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+ (tested on 3.12)
- pip

### Installation

```bash
git clone https://github.com/<your-username>/routeoptima.git
cd routeoptima
pip install -r requirements.txt
```

### Run Demo

```bash
python -m src.demo -n 1000 --seed 42
```

Options:
- `-n` / `--vertices`: number of locations (default: 1000)
- `-s` / `--seed`: random seed (default: 42)
- `--source`: source vertex (default: 0)
- `--target`: target vertex (default: last vertex)

### Run Benchmark (One Command)

```bash
bash run_benchmark.sh
```

This will:
1. Benchmark both algorithms on sizes [100, 250, 500, 1000, 2500, 5000, 10000]
2. Save results to `bench/results.csv`
3. Generate plots in `bench/`
4. Run a demo on V=1000

### Run Individually

```bash
# Benchmark only
python -m src.benchmark --output bench/results.csv

# Plots only (after benchmark)
python plot.py bench/results.csv
```

## Problem Description

A delivery company must route packages between locations in a city. The road network is modeled as a weighted undirected graph **G = (V, E, w)** where:

- **V** = set of locations (intersections/warehouses/delivery points)
- **E** = set of roads connecting locations
- **w(e) ≥ 0** = road distance/travel time for edge e

**Objective:** Given a source and target location, find the path with minimum total weight (shortest route).

## Algorithms

### Dijkstra (Algorithm A)
- Uses a **binary min-heap** priority queue
- Greedily expands the closest unvisited vertex
- **Time: O((V + E) log V)** — each vertex popped once, each edge relaxed once, each heap operation O(log V)
- **Space: O(V + E)**
- Requires non-negative edge weights

### Bellman-Ford (Algorithm B)
- Iteratively relaxes **all edges** for V−1 passes
- Can detect negative-weight cycles
- **Time: O(V · E)** — V−1 passes over all E edges
- **Space: O(V)**
- Includes early-termination optimization

## Attribution

- Python `heapq` module used for Dijkstra's priority queue (standard library)
- `matplotlib` and `numpy` used for plotting only
- All algorithmic logic is original code

## Language & Version

- **Language:** Python 3.12
- **OS:** Ubuntu 24.04 / any platform with Python 3.10+
