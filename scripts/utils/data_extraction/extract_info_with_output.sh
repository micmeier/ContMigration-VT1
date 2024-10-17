#!/bin/bash

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

# Check if the required argument is provided
if [ $# -ne 2 ]; then
  echo "Usage: $0 <checkpoint file>"
  exit 1
fi

checkpoint_file=$1
index=$2
output_dir="/home/ubuntu/ContMigration/utils/data_extraction/extracted_data"

# Create the output directory if it doesn't exist
#mkdir -p "$output_dir"

# Get the base name of the checkpoint file
# checkpoint_basename=$(basename "$checkpoint_file")

# Get the base name of the checkpoint file and adjust the name
checkpoint_basename=$(basename "$checkpoint_file" .tar)
checkpoint_basename=$(echo "$checkpoint_basename" | sed 's/:/-/g')

# Construct the output file path
output_file="$output_dir/data-${checkpoint_basename}.csv"

# Run the checkpointctl inspect command and store the output
output=$(checkpointctl inspect "$checkpoint_file" --stats)

# Extract and print the required values in CSV format
echo "Index,Image,Checkpointed,Checkpoint size,Freezing time,Frozen time,Memdump time,Memwrite time,Total dump time (ms)" > "$output_file"
# Image
image=$(echo "$output" | grep -E '^\s*├── Image:' | awk -F': ' '{print $2}')
# Checkpointed
checkpointed=$(echo "$output" | grep -E '^\s*├── Checkpointed:' | awk -F': ' '{print $2}')
# Checkpoint size
checkpoint_size=$(echo "$output" | grep -E '^\s*├── Checkpoint size:' | awk -F': ' '{print $2}')
# CRIU dump statistics
freezing_time=$(echo "$output" | grep -E '^\s*├── Freezing time:' | awk -F': ' '{print $2}')
frozen_time=$(echo "$output" | grep -E '^\s*├── Frozen time:' | awk -F': ' '{print $2}')
memdump_time=$(echo "$output" | grep -E '^\s*├── Memdump time:' | awk -F': ' '{print $2}')
memwrite_time=$(echo "$output" | grep -E '^\s*├── Memwrite time:' | awk -F': ' '{print $2}')
# Convert times to milliseconds and sum them using awk
total_dump_time_ms=$(awk -v fz=$(convert_to_ms "$freezing_time") \
                        -v fn=$(convert_to_ms "$frozen_time") \
                        -v md=$(convert_to_ms "$memdump_time") \
                        -v mw=$(convert_to_ms "$memwrite_time") \
                        'BEGIN {print fz + fn + md + mw}')

# Print additional information to the terminal
echo "Extracted Information:"
echo "----------------------"
echo "Image: $image"
echo "Checkpointed: $checkpointed"
echo "Checkpoint size: $checkpoint_size"
echo "CRIU dump statistics:"
echo "  Freezing time: $freezing_time"
echo "  Frozen time: $frozen_time"
echo "  Memdump time: $memdump_time"
echo "  Memwrite time: $memwrite_time"
echo "Total dump time: ${total_dump_time_ms} ms"

# Print the extracted values in CSV format and save to the output file
echo "$index,$image,$checkpointed,$checkpoint_size,$freezing_time,$frozen_time,$memdump_time,$memwrite_time,$total_dump_time_ms" >> "$output_file"

# Print the path of the output file
echo "Output saved to: $output_file"
