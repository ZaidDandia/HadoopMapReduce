#!/usr/bin/env python3
import sys

for line in sys.stdin:
    fields = line.strip().split(',')
    if len(fields) == 5:
        try:
            sepal_length, sepal_width, petal_length, petal_width = map(float, fields[:4])
            species = fields[4]
            # Emit data for each feature
            print(f"sepal_length\t{sepal_length}")
            print(f"sepal_width\t{sepal_width}")
            print(f"petal_length\t{petal_length}")
            print(f"petal_width\t{petal_width}")
            print(f"species\t{species}")
        except ValueError:
            continue
