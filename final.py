import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import subprocess


# Helper function to read HDFS output files
def read_hdfs_file(hdfs_path):
    try:
        result = subprocess.run(
            ["hdfs", "dfs", "-cat", hdfs_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")
        else:
            print(f"Error reading HDFS file {hdfs_path}: {result.stderr}")
            return []
    except Exception as e:
        print(f"Error accessing HDFS: {e}")
        return []


# List of files to include
file_paths = {
    "ml_results": "/output/ml_results/part-00000",
    "eda_results": "/output/eda_results/part-00000",
    "preprocess_results": "/output/preprocess_results/part-00000",
}

# Load data from all files
data = {}
for key, path in file_paths.items():
    lines = read_hdfs_file(path)
    if lines:
        data[key] = lines
    else:
        print(f"Failed to load data for {key}.")

# Process `ml_results`
features, true_labels, predicted_labels = [], [], []
if "ml_results" in data:
    for line in data["ml_results"]:
        if "Feature:" in line and "True Label:" in line and "Predicted Label:" in line:
            try:
                # Clean and extract feature, true label, and predicted label
                feature = eval(
                    line.split("Feature:")[1].split("True Label:")[0].strip()
                )
                true_label = (
                    line.split("True Label:")[1]
                    .split("Predicted Label:")[0]
                    .strip()
                    .strip(",")
                )
                predicted_label = line.split("Predicted Label:")[1].strip().strip(",")

                features.append(feature)
                true_labels.append(true_label)
                predicted_labels.append(predicted_label)
            except Exception as e:
                print(f"Error parsing line: {line} - {e}")

# Convert to NumPy arrays
y_true = np.array(true_labels)
y_pred = np.array(predicted_labels)

# Check if y_true and y_pred are not empty
if len(y_true) > 0 and len(y_pred) > 0:
    # Confusion Matrix
    unique_labels = sorted(
        set(y_true) | set(y_pred)
    )  # All unique labels in true and predicted
    cm = confusion_matrix(y_true, y_pred, labels=unique_labels)
    print("\nConfusion Matrix:")
    print(cm)

    # Classification Report
    print("\nClassification Report:")
    print(
        classification_report(
            y_true, y_pred, target_names=unique_labels, zero_division=0
        )
    )

    # Visualize the confusion matrix
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(unique_labels))
    plt.xticks(tick_marks, unique_labels, rotation=45)
    plt.yticks(tick_marks, unique_labels)
    plt.ylabel("True label")
    plt.xlabel("Predicted label")

    # Add text annotations
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j,
                i,
                format(cm[i, j], "d"),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )

    # Save and display the confusion matrix visualization
    output_image_path = "confusion_matrix.png"  # Define the output path for the image
    plt.savefig(output_image_path)  # Save the figure to a file
    plt.show()  # Optionally display it
    print(f"Confusion matrix saved as {output_image_path}.")

# Process `eda_results`
if "eda_results" in data:
    print("\nEDA Results:")
    for line in data["eda_results"]:
        print(line)

# Process `preprocess_results`
if "preprocess_results" in data:
    print("\nPreprocessed Data Sample:")
    preprocess_sample = [
        line for line in data["preprocess_results"][:5]
    ]  # Show first 5 lines
    for line in preprocess_sample:
        print(line)
