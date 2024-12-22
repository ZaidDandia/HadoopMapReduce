#!/usr/bin/env python3
import sys
import random

for line in sys.stdin:
    fields = line.strip().split(',')
    if len(fields) == 5:
        try:
            features = [float(value) for value in fields[:4]]  # Convert features to float
            label = fields[4].strip()  # Extract the label
            # Assign 80% of data to training and 20% to testing
            split = "train" if random.random() < 0.8 else "test"
            # Print the split, features, and label as tab-separated values
            print(f"{split}\t{features}\t{label}")
        except ValueError:
            # Skip lines with invalid numeric values
            continue
