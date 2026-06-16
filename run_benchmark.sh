#!/usr/bin/env bash 
# RouteOptima — One-command benchmark
# Usage: bash run_benchmark.sh
set -e

echo ""
echo "================================================"
echo "  RouteOptima — Full Benchmark Pipeline"
echo "================================================"
echo ""

# Step 1: Run benchmark
echo "[Step 1/3] Running benchmark (Dijkstra vs Bellman-Ford)..."
python -m src.benchmark --output bench/results.csv

# Step 2: Generate plots
echo ""
echo "[Step 2/3] Generating plots..."
python plot.py bench/results.csv

# Step 3: Run demo
echo ""
echo "[Step 3/3] Running demo (V=1000)..."
python -m src.demo -n 1000 --seed 42

echo ""
echo "All done! Check bench/ for results.csv and plots."
echo ""
