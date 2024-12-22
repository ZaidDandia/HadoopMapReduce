#!/usr/bin/env python3
import sys

# Read input line by line
for line in sys.stdin:
    # Skip empty lines
    if not line.strip():
        continue
    # Split the line by commas
    fields = line.strip().split(',')
    # Ensure all fields are present (5 fields in this dataset)
    if len(fields) == 5:
        try:
            # Check if numerical fields are valid
            sepal_length, sepal_width, petal_length, petal_width = map(float, fields[:4])
            species = fields[4]
            # Emit the cleaned data
            print(f"{sepal_length},{sepal_width},{petal_length},{petal_width},{species}")
        except ValueError:
            # Skip invalid rows
            continue
