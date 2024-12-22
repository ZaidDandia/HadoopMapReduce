#!/bin/bash
# Variables
HDFS_INPUT_DIR=/input
LOCAL_DATASET=iris.data

# Upload dataset to HDFS
hdfs dfs -mkdir -p $HDFS_INPUT_DIR
hdfs dfs -put $LOCAL_DATASET $HDFS_INPUT_DIR

echo "Dataset uploaded to HDFS at $HDFS_INPUT_DIR."
