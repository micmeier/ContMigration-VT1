#!/bin/bash

# read on which cluster redis is running
kubectl config use-context cluster1
echo "Looking for redis in cluster 1."
if kubectl get pod/redis-0 &> /dev/null; then
	SRC_NODE=$(kubectl get pod/redis-0 -o jsonpath='{.spec.nodeName}')
	DST_CLUSTER="cluster2"
	echo "Redis on $SRC_NODE detected."
else
	echo "Redis not found in cluster 1, switching to cluster 2."
	kubectl config use-context cluster2
	if kubectl get pod/redis-0 &> /dev/null; then
		SRC_NODE=$(kubectl get pod/redis-0 -o jsonpath='{.spec.nodeName}')
		DST_CLUSTER="cluster1"
		echo "Redis on $SRC_NODE detected."
	else
		echo "Redis not detected. Terminating."
		exit 1
	fi
		
fi

# prepare shutdown 
echo "Creating redis backup."
kubectl exec -it redis-0 -- redis-cli SAVE
echo "Backup 'dump.rdb' created."

echo "Uploading backup to redis network file system."
kubectl cp redis-0:/data/dump.rdb ~/apps/mem_intensive/nfs/new_dump.rdb
echo "Backup uploaded."

# shutdown
echo "Shutting down redis on $SRC_NODE."
kubectl scale sts redis --replicas=0
echo "Redis on $SRC_NODE terminated."

mv -f ~/apps/mem_intensive/nfs/new_dump.rdb ~/apps/mem_intensive/nfs/dump.rdb

echo "Starting redis on $DST_CLUSTER."
kubectl config use-context $DST_CLUSTER
kubectl scale sts redis --replicas=1
DST_NODE=$(kubectl get pod/redis-0 -o jsonpath='{.spec.nodeName}')
echo "Redis started on $DST_NODE."

