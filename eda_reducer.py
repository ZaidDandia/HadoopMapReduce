#!/usr/bin/env python3
import sys
from collections import defaultdict

counts = defaultdict(int)
sums = defaultdict(float)
min_vals = defaultdict(lambda: float('inf'))
max_vals = defaultdict(lambda: float('-inf'))

for line in sys.stdin:
    key, value = line.strip().split('\t')
    try:
        value = float(value)
        counts[key] += 1
        sums[key] += value
        min_vals[key] = min(min_vals[key], value)
        max_vals[key] = max(max_vals[key], value)
    except ValueError:
        counts[key] += 1  # For categorical values like species

# Output aggregated statistics
for key in counts.keys():
    if key.startswith("species"):
        print(f"{key}\tcount:{counts[key]}")
    else:
        avg = sums[key] / counts[key]
        print(f"{key}\tcount:{counts[key]},mean:{avg:.2f},min:{min_vals[key]:.2f},max:{max_vals[key]:.2f}")
