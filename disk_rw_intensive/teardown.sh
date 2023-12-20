#!/bin/bash

rm state.txt

# teardown on cluster 1
kubectl config use-context cluster1
kubectl delete sts mongo
kubectl delete svc mongo-service
kubectl delete pvc mongo-pvc
kubectl delete pv mongo-pv

# teardown on cluster 2
kubectl config use-context cluster2
kubectl delete sts mongo
kubectl delete svc mongo-service
kubectl delete pvc mongo-pvc
kubectl delete pv mongo-pv
