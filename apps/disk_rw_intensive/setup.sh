#!/bin/bash

# start mongodb on cluster 1
kubectl config use-context cluster1
kubectl apply -f yaml/sts.yaml
kubectl apply -f yaml/sc.yaml
kubectl apply -f yaml/svc.yaml

# start mongodb on cluster 2
kubectl config use-context cluster2
kubectl apply -f yaml/sts.yaml
kubectl apply -f yaml/sc.yaml
kubectl apply -f yaml/svc.yaml

read -p "On which cluster should mongo start first? (Enter 1 or 2): " cluster
kubectl config use-context cluster$cluster
kubectl apply -f yaml/pv.yaml
kubectl apply -f yaml/pvc.yaml
kubectl scale sts mongo --replicas=1

# Wait for the pod to be in the "Running" state
kubectl wait --for=condition=Ready pod/mongo-0
echo "Mongo successfully deployed"

# Run kubectl command and extract worker node
worker_node=$(kubectl get pod/mongo-0 -o jsonpath='{.spec.nodeName}')

# Print the worker node to verify
echo "Worker Node: $worker_node"

# Capture the port in a variable
mongo_port=$(kubectl get all -o wide | grep 27017 | awk -F '27017:' '{print $2}' | awk -F '/' '{print $1}')

# Print the port to verify
echo "MongoDB Port: $mongo_port"

