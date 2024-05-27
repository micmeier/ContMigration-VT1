#!/bin/bash

# Output CSV file
#output_csv="checkpoint_data.csv"

# Remove existing CSV file
#rm -f "$output_csv"

# Loop over each checkpoint file
# still hardcoded path!
for checkpoint_file in /home/ubuntu/nfs/checkpoints/worker3/*.tar; do
    echo "Processing checkpoint file: $checkpoint_file"
    
    # Run extract_info.sh and append output to CSV
    ./extract_info_with_output.sh "$checkpoint_file"
done

echo "Data extraction complete."
