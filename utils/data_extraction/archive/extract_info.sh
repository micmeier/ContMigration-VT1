#!/bin/bash

# Check if the required argument is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <checkpoint file>"
  exit 1
fi

checkpoint_file=$1

# Run the checkpointctl inspect command and store the output
output=$(checkpointctl inspect $checkpoint_file --stats)

# Extract and print the required values
echo "Extracted Information:"
echo "----------------------"

# Image
image=$(echo "$output" | grep -E '^\s*├── Image:' | awk -F': ' '{print $2}')
echo "Image: $image"

# Checkpointed
checkpointed=$(echo "$output" | grep -E '^\s*├── Checkpointed:' | awk -F': ' '{print $2}')
echo "Checkpointed: $checkpointed"

# Checkpoint size
checkpoint_size=$(echo "$output" | grep -E '^\s*├── Checkpoint size:' | awk -F': ' '{print $2}')
echo "Checkpoint size: $checkpoint_size"

# CRIU dump statistics
echo "CRIU dump statistics:"

freezing_time=$(echo "$output" | grep -E '^\s*├── Freezing time:' | awk -F': ' '{print $2}')
echo "  Freezing time: $freezing_time"

frozen_time=$(echo "$output" | grep -E '^\s*├── Frozen time:' | awk -F': ' '{print $2}')
echo "  Frozen time: $frozen_time"

memdump_time=$(echo "$output" | grep -E '^\s*├── Memdump time:' | awk -F': ' '{print $2}')
echo "  Memdump time: $memdump_time"

memwrite_time=$(echo "$output" | grep -E '^\s*├── Memwrite time:' | awk -F': ' '{print $2}')
echo "  Memwrite time: $memwrite_time"

# Function to convert time units to milliseconds
convert_to_ms() {
  local time_str=$1
  if [[ $time_str == *"ms" ]]; then
    echo "${time_str% ms}"
  elif [[ $time_str == *"µs" ]]; then
    echo "$time_str" | awk '{printf "%.3f", $1 / 1000}'
  else
    echo "0"
  fi
}

# Convert times to milliseconds and sum them using awk
total_dump_time_ms=$(awk -v fz=$(convert_to_ms "$freezing_time") \
                        -v fn=$(convert_to_ms "$frozen_time") \
                        -v md=$(convert_to_ms "$memdump_time") \
                        -v mw=$(convert_to_ms "$memwrite_time") \
                        'BEGIN {print fz + fn + md + mw}')

echo "Total dump time: ${total_dump_time_ms} ms"
