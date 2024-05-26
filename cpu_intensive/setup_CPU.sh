#!/bin/bash

echo -e "How many cores should be utilized?"
echo -e "If x exceeds available cores of host, the maximum no. of cores will be used."
read -p "Choose between 1-x: " chosen_cores

echo -e "How much CPU usage per core?"
read -p "Enter int between 1-100%: " chosen_percentage

# Number of Replicaset
echo -e "Number of Replicasets?"
read -p "Enter an int: " number_replicaset

# Run the yaml
kubectl apply -f yaml/multicore_cpu.yaml

# Patch the StatefulSet with the chosen values
kubectl patch statefulset cpu --type='json' -p "[{\"op\": \"replace\", \"path\": \"/spec/template/spec/containers/0/env/0/value\", \"value\": \"$chosen_cores\"}, {\"op\": \"replace\", \"path\": \"/spec/template/spec/containers/0/env/1/value\", \"value\": \"$chosen_percentage\"}, {\"op\": \"replace\", \"path\": \"/spec/replicas\", \"value\": $number_replicaset}]"
