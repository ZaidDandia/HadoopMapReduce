#!/bin/bash

# Define directories
INPUT_DIR=/input/iris.data

PREPROCESS_OUTPUT=/output/preprocess_results
EDA_OUTPUT=/output/eda_results
ML_OUTPUT=/output/ml_results
LOCAL_OUTPUT_DIR="/tmp/iris_pipeline_results"  # Local directory for final outputs

# Ensure the local output directory exists
mkdir -p $LOCAL_OUTPUT_DIR

# Clean up existing directories in HDFS if they exist
hdfs dfs -rm -r $PREPROCESS_OUTPUT 2>/dev/null
hdfs dfs -rm -r $EDA_OUTPUT 2>/dev/null
hdfs dfs -rm -r $ML_OUTPUT 2>/dev/null

# Step 1: Data Preprocessing
echo "Running Preprocessing..."
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input $INPUT_DIR \
    -output $PREPROCESS_OUTPUT \
    -mapper "python3 preprocess_mapper.py" \
    -reducer "python3 preprocess_reducer.py"

# Fetch the preprocessing results locally
hdfs dfs -cat $PREPROCESS_OUTPUT/part-* > $LOCAL_OUTPUT_DIR/preprocessed_data.csv
if [ ! -s $LOCAL_OUTPUT_DIR/preprocessed_data.csv ]; then
  echo "No valid data available after preprocessing. Exiting."
  exit 1
fi
echo "Preprocessing completed. Results saved to $LOCAL_OUTPUT_DIR/preprocessed_data.csv."

# Step 2: Exploratory Data Analysis (EDA)
echo "Running EDA..."
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input $PREPROCESS_OUTPUT \
    -output $EDA_OUTPUT \
    -mapper "python3 eda_mapper.py" \
    -reducer "python3 eda_reducer.py"

# Fetch the EDA results locally
hdfs dfs -cat $EDA_OUTPUT/part-* > $LOCAL_OUTPUT_DIR/eda_results.txt
if [ ! -s $LOCAL_OUTPUT_DIR/eda_results.txt ]; then
  echo "No valid data available after EDA. Exiting."
  exit 1
fi
echo "EDA completed. Results saved to $LOCAL_OUTPUT_DIR/eda_results.txt."

# Step 3: Machine Learning Model Execution
echo "Running ML Model..."
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input $PREPROCESS_OUTPUT \
    -output $ML_OUTPUT \
    -mapper "python3 ml_mapper.py" \
    -reducer "python3 ml_reducer.py"

# Fetch the ML results locally
hdfs dfs -cat $ML_OUTPUT/part-* > $LOCAL_OUTPUT_DIR/ml_results.txt
if [ ! -s $LOCAL_OUTPUT_DIR/ml_results.txt ]; then
  echo "No valid data available after ML model execution. Exiting."
  exit 1
fi
echo "ML Model execution completed. Results saved to $LOCAL_OUTPUT_DIR/ml_results.txt."

# Print completion message
echo "Pipeline completed successfully. Results are in $LOCAL_OUTPUT_DIR."
python3 final.py