#!/bin/bash


# read on which cluster redis is running
kubectl config use-context cluster1
SRC_NODE=$(kubectl get pod/redis-0 -o jsonpath='{.spec.nodeName}')

if [$SRC_NODE != "worker1" && $SRC_NODE != "worker2"]
then
	kubectl config use-context cluster2
	SRC_NODE=$(kubectl get pod/redis-0 -o jsonpath='{.spec.nodeName}')

echo "Redis on $SRC_NODE detected"

#prepare cluster1 shutdown
#kubectl config use-context cluster1

#echo "Creating backup on source pod"
#kubectl exec -it redis-0 -- redis-cli SAVE
#echo "Backup created"

#echo "Copying backup to node"
#kubectl cp redis-0:/data/dump.rdb dump.rdb
#echo "Done copying backup to node"

#echo "Killing redis on source node"
#kubectl scale statefulsets redis --replicas=0
#echo "Redis killed on source node"

#kubectl config use-context cluster2

#echo "Starting redis on destination node"
#kubectl scale statefulsets redis --replicas=1
#echo "Redis started on destination node"

#echo "Waiting for container to start"
#sleep 5

#echo "Copying dump into redis"
#kubectl cp dump.rdb redis-0:/data/dump.rdb
#echo "Copying complete"

#echo "Restoring data in redis"
#kubectl exec -it redis-0 -- redis-cli --rdb /data/dump.rdb
#echo "Data restored"


