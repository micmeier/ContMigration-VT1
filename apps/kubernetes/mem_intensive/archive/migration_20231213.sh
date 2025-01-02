#!/bin/bash
source ~/apps/utils/detector.sh

detect_cluster redis

kubectl config use-context $CLUSTER

# prepare shutdown 
echo "Creating redis backup."
kubectl exec -it redis-0 -- redis-cli SAVE
echo "Backup 'dump.rdb' created."

echo "Uploading backup to redis network file system."
kubectl cp redis-0:/data/dump.rdb ~/apps/mem_intensive/nfs/new_dump.rdb
echo "Backup uploaded."

# shutdown
echo "Shutting down redis in $CLUSTER."
kubectl scale sts redis --replicas=0
echo "Redis in $CLUSTER terminated."

mv -f ~/apps/mem_intensive/nfs/new_dump.rdb ~/apps/mem_intensive/nfs/dump.rdb

determine_dest_cluster

echo "Starting redis in $DEST_CLUSTER."
kubectl config use-context $DEST_CLUSTER
kubectl scale sts redis --replicas=1
echo "Redis started in $DEST_CLUSTER."

echo "Waiting for redis to be deployed again"
kubectl wait --for=condition=Ready pod/redis-0

echo "Restarting load generator."
./generate_load.sh
