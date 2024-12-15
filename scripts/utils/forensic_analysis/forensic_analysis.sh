#!/bin/bash

# Check if a checkpoint file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_checkpoint_file>"
    exit 1
fi

# Set variables
CHECKPOINT_FILE="$1"
OUTPUT_DIR="/home/ubuntu/forensic_analysis"
TMP_DIR="/home/ubuntu/forensic_analysis/temp"

# Step 1: Prepare environment
prepare_environment() {
    echo "Preparing environment..."
    mkdir -p "$TMP_DIR"
    mkdir -p "$OUTPUT_DIR"
    echo "Environment prepared."
}

# Step 2: Extract container checkpoint
extract_checkpoint() {
    if [ ! -f "$CHECKPOINT_FILE" ]; then
        echo "Error: Checkpoint file $CHECKPOINT_FILE does not exist."
        exit 1
    fi

    echo "Extracting container checkpoint..."
    tar -xf "$CHECKPOINT_FILE" -C "$TMP_DIR" || {
        echo "Error: Failed to extract checkpoint file."
        exit 1
    }
    chmod -R 770 "$TMP_DIR"
    echo "Checkpoint extracted to $TMP_DIR."
}


inspect_checkpoint() {
    echo "Getting checkpoint information"
    echo "----- Checkpoint information -----" >> "$OUTPUT_DIR/forensic_report.txt"
    sudo checkpointctl inspect "$CHECKPOINT_FILE" >> "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error: Failed to extract process list."
        exit 1
    }
    echo "Checkpoint information saved to $OUTPUT_DIR/forensic_report.txt."
}

analyze_process_tree() {
    echo "Extracting process list..."
    sudo checkpointctl inspect "$CHECKPOINT_FILE" --ps-tree-cmd |  awk '/Process tree/{flag=1; next} flag' >> "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error: Failed to extract process list."
        exit 1
    }
    echo "Process list saved to $OUTPUT_DIR/forensic_report.txt."

    awk '/Process tree/{flag=1; next} /Checkpoint information/{flag=0} flag' "$OUTPUT_DIR/forensic_report.txt" > "$OUTPUT_DIR/process_tree.txt"
}


# Step 3: Analyze checkpoint data
# This function extracts filesystem metadata from the checkpoint file and saves it to the output directory.
analyze_filesystem_metadata() {
    echo "Analyzing filesystem metadata..."
    tar -tf "$CHECKPOINT_FILE" > "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error: Failed to analyze filesystem metadata."
        exit 1
    }
    echo "Filesystem metadata saved to $OUTPUT_DIR/forensic_report.txt."
}


analyze_network_activity() {
    echo "Analyzing network activity..."
    grep -r 'network' "$TMP_DIR/" > "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error: Failed to analyze network activity."
        exit 1
    }
    echo "Network activity saved to $OUTPUT_DIR/forensic_report.txt."
}

# Step 4: Data interpretation
interpret_data() {
    echo "Interpreting extracted data..."
    {
        echo "Filesystem Metadata:"
        cat "$OUTPUT_DIR/filesystem_metadata.txt"
        echo

        echo "Process List:"
        cat "$OUTPUT_DIR/process_list.txt"
        echo

        echo "Network Activity:"
        cat "$OUTPUT_DIR/network_activity.txt"
    } > "$OUTPUT_DIR/forensic_report.txt"

    echo "Data interpretation complete. Report saved to $OUTPUT_DIR/forensic_report.txt."
}

# Main function to run the script
main() {
    prepare_environment
    extract_checkpoint
    inspect_checkpoint
    # analyze_process_list
    # analyze_network_activity
    # interpret_data
}

# Run the script
main
