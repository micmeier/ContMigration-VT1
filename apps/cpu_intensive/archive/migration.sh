#!/bin/bash
source ~/apps/utils/detector.sh

detect_cluster cpu

kubectl config use-context $CLUSTER

echo "Shutting down cpu intensive app in $CLUSTER."
kubectl scale sts cpu --replicas=0
echo "cpu intensive app in $CLUSTER shut down."

determine_dest_cluster

echo "Starting cpu intensive app in $DEST_CLUSTER."
kubectl config use-context $DEST_CLUSTER
kubectl scale sts cpu --replicas=1
echo "Cpu intensive app started in $DEST_CLUSTER."


