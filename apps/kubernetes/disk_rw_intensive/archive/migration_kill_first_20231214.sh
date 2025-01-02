#!/bin/bash

# read on which cluster mongo is running
kubectl config use-context cluster1
echo "Looking for Mongo in cluster 1."
if kubectl get pod/mongo-0 &> /dev/null; then
        SRC_NODE=$(kubectl get pod/mongo-0 -o jsonpath='{.spec.nodeName}')
        DST_CLUSTER="cluster2"
        echo "Mongo on $SRC_NODE detected."
else
        echo "Mongo not found in cluster 1, switching to cluster 2."
        kubectl config use-context cluster2
        if kubectl get pod/mongo-0 &> /dev/null; then
                SRC_NODE=$(kubectl get pod/mongo-0 -o jsonpath='{.spec.nodeName}')
                DST_CLUSTER="cluster1"
                echo "Mongo on $SRC_NODE detected."
        else
                echo "Mongo not detected. Terminating."
                exit 1
        fi

fi

# print start time of migration
start_time=$(date +%s%3N)
formatted_time=$(date +%T)
echo "---"
echo "Started Migration at: $formatted_time"

echo "---"
# prepare shutdown
# shutdown
echo "Shutting down Mongo on $SRC_NODE."
kubectl scale sts mongo --replicas=0
echo "Mongo on $SRC_NODE terminated."
echo "---"

# state?
state_file="state.txt"

if [ -f "$state_file" ]; then
    content=$(cat "$state_file")
    IFS=',' read -r start_index remaining_entries <<< "$content"
    echo "Stopped at: $start_index. Remaining: $remaining_entries"
else
    echo "State file not found."
fi
echo "---"

# start on destination cluster
echo "Starting Mongo on $DST_CLUSTER."
kubectl config use-context $DST_CLUSTER
kubectl scale sts mongo --replicas=1
echo "---"

# Wait for the pod to be in the "Running" state
echo "Waiting for Mongo Pod to be ready."
kubectl wait --for=condition=Ready pod/mongo-0
echo "---"

# Run kubectl command and extract worker node
worker_node=$(kubectl get pod/mongo-0 -o jsonpath='{.spec.nodeName}')

# Print the worker node to verify
echo "Pod started on Worker Node: $worker_node."

# Capture the port in a variable
mongo_port=$(kubectl get all -o wide | grep 27017 | awk -F '27017:' '{print $2}' | awk -F '/' '{print $1}')

# Print the port to verify
echo "MongoDB Port: $mongo_port."

DST_NODE=$(kubectl get pod/mongo-0 -o jsonpath='{.spec.nodeName}')
echo "Mongo started on $DST_NODE."
echo "---"

# let script run from state from before
# print start time of script
echo "Started Migration at: $formatted_time"
start_time=$(date +%s%3N)
formatted_time=$(date +%T)
echo "Starting Script at: $formatted_time"
echo "Continuing script now."
echo "---"

# let script run from state from before
python3 /home/ubuntu/apps/disk_rw_intensive/python_scripts/data_generator.py "data" "-1" "$worker_node:$mongo_port" "state.txt"
