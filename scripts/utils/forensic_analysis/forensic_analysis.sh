#!/bin/bash

# Check if a checkpoint file is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path_to_checkpoint_file>"
    exit 1
fi

# Set variables
CHECKPOINT_FILE="$1"
OUTPUT_DIR="$2"
TMP_DIR="$OUTPUT_DIR/temp"

# Step 1: Prepare environment
prepare_environment() {
    echo "Preparing environment..."
    mkdir -p "$TMP_DIR/changed"
    echo "Environment prepared."
}

# Step 2: Extract container checkpoint
inspect_checkpoint() {
    if [ ! -f "$CHECKPOINT_FILE" ]; then
        echo "Error: Checkpoint file $CHECKPOINT_FILE does not exist."
        exit 1
    fi
    echo "Generating forensic report..."
    echo "----- Checkpoint information -----" >> "$OUTPUT_DIR/forensic_report.txt"
    sudo checkpointctl inspect "$CHECKPOINT_FILE" >> "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error: Failed to extract process list."
        exit 1
    }
}

analyze_process_tree() {
    echo "----- Process tree -----" >> "$OUTPUT_DIR/forensic_report.txt"
    sudo checkpointctl inspect "$CHECKPOINT_FILE" --ps-tree-cmd | awk '/Process tree/{flag=1} flag' >> "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error extracting process tree from checkpoint file"
        exit 1
    }
}


# Step 3: Analyze checkpoint data
# This function extracts filesystem metadata from the checkpoint file and saves it to the output directory.
analyze_sockets() {
    echo "----- Open sockets -----" >> "$OUTPUT_DIR/forensic_report.txt"
    sudo checkpointctl inspect "$CHECKPOINT_FILE" --sockets | awk '/Process tree/{flag=1; next} flag' >> "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error extracting process tree from checkpoint file"
        exit 1
    }
}

analyze_files() {
    echo "----- Open files -----" >> "$OUTPUT_DIR/forensic_report.txt"
    sudo checkpointctl inspect "$CHECKPOINT_FILE" --files | awk '/Open files/{flag=1; next} flag' >> "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error extracting process tree from checkpoint file"
        exit 1
    }
    echo "Open files saved to $OUTPUT_DIR/forensic_report.txt."
}

analyze_memory() {
    echo "----- Memory size -----" >> "$OUTPUT_DIR/forensic_report.txt"
    sudo checkpointctl memparse "$CHECKPOINT_FILE" | awk '/Displaying processes/{flag=1; next} flag' >> "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error extracting memory size from checkpoint file"
        exit 1
    }
}

extract_checkpoint() {
    tar -xf "$CHECKPOINT_FILE" -C "$TMP_DIR" || {
        echo "Error: Failed to extract checkpoint file."
        exit 1
    }
    chmod -R 770 "$TMP_DIR"
    echo "----- Changed files -----" >> "$OUTPUT_DIR/forensic_report.txt"
    tar xvf "$TMP_DIR/rootfs-diff.tar" -C "$TMP_DIR/changed" >> "$OUTPUT_DIR/forensic_report.txt" || {
        echo "Error: Failed to extract rootfs-diff file."
        exit 1
    }
}

# Main function to run the script
main() {
    prepare_environment
    inspect_checkpoint
    analyze_process_tree
    analyze_sockets
    analyze_memory
#    analyze_files
    extract_checkpoint
}

# Run the script
main
