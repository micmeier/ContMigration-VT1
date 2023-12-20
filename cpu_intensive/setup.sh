#!/bin/bash

# start cpu int  on cluster 1
kubectl config use-context cluster1
kubectl apply -f cpu.yaml

# start cpu int on cluster 2
kubectl config use-context cluster2
kubectl apply -f cpu.yaml

read -p "On which cluster should CPU Intensive Container start first? (Enter 1 or 2): " cluster

kubectl config use-context cluster$cluster
kubectl scale sts cpu --replicas=1
