#!/bin/bash

# teardown on cluster 1
kubectl config use-context cluster1
kubectl delete sts redis
kubectl delete svc redis-service
kubectl delete pvc redis-pvc
kubectl delete pv redis-pv
kubectl delete sc storageclass-nfs

# teardown on cluster 2
kubectl config use-context cluster2
kubectl delete sts redis
kubectl delete svc redis-service
kubectl delete pvc redis-pvc
kubectl delete pv redis-pv
kubectl delete sc storageclass-nfs
