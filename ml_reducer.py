#!/usr/bin/env python3
import sys
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import json

# Initialize training and testing datasets
train_X, train_y = [], []
test_X, test_y = [], []

# Read mapper output
for line in sys.stdin:
    try:
        split, features, label = line.strip().split('\t')
        features = json.loads(features)  # Parse features safely using JSON
        if split == "train":
            train_X.append(features)
            train_y.append(label)
        elif split == "test":
            test_X.append(features)
            test_y.append(label)
    except ValueError:
        # Skip malformed lines
        continue

# Ensure we have training data before fitting the model
if len(train_X) == 0 or len(test_X) == 0:
    print("Error: Insufficient data for training or testing.")
    sys.exit(1)

# Train the Decision Tree model
model = DecisionTreeClassifier()
model.fit(train_X, train_y)

# Test the model
predictions = model.predict(test_X)
accuracy = accuracy_score(test_y, predictions)

# Output accuracy and predictions
print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(test_y, predictions))

# Optionally, output predictions for analysis
for feature, true_label, pred_label in zip(test_X, test_y, predictions):
    print(f"Feature: {feature}, True Label: {true_label}, Predicted Label: {pred_label}")
