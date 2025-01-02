#!/bin/bash

#kubectl cp cpu-statefulset-0:/cpu_intensive/prime_numbers.txt prime_numbers.txt

# teardown on cluster 1
kubectl config use-context cluster1
kubectl delete sts cpu

# teardown on cluster 2
kubectl config use-context cluster2
kubectl delete sts cpu
