#!/bin/bash

# Find the PIDs of the Python script
pids=$(pgrep python3)

# Check if any PIDs were found
if [ -z "$pids" ]; then
    echo "No such process/processes found."
else
    # Iterate over each PID and kill the corresponding process
    for pid in $pids; do
        echo "Killing process with PID $pid..."
        kill $pid
    done
fi
