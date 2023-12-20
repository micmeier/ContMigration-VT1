#!/bin/bash

# start redis on cluster 1
kubectl config use-context cluster1
kubectl apply -f /home/ubuntu/apps/mem_intensive/yaml/sts.yaml
kubectl apply -f /home/ubuntu/apps/mem_intensive/yaml/storageClass.yaml
kubectl apply -f /home/ubuntu/apps/mem_intensive/yaml/svc.yaml

# start redis on cluster 2
kubectl config use-context cluster2
kubectl apply -f /home/ubuntu/apps/mem_intensive/yaml/sts.yaml
kubectl apply -f /home/ubuntu/apps/mem_intensive/yaml/storageClass.yaml
kubectl apply -f /home/ubuntu/apps/mem_intensive/yaml/svc.yaml

read -p "On which cluster should redis start first? (Enter 1 or 2): " cluster

kubectl config use-context cluster$cluster
kubectl apply -f /home/ubuntu/apps/mem_intensive/yaml/pv.yaml
kubectl apply -f /home/ubuntu/apps/mem_intensive/yaml/pvc.yaml
kubectl scale sts redis --replicas=1


