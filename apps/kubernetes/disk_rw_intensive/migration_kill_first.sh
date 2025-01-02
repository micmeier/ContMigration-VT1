#!/bin/bash
source ~/apps/utils/detector.sh

while true; do
        #determine cluster
        detect_cluster mongo
        kubectl config use-context $CLUSTER

        # print start time of migration
        start_time=$(date +%s%3N)
        formatted_time=$(date '+%H:%M:%S.%3N')
        echo "---"
        echo "Started Migration at: $formatted_time."

        #scale down sts in source
        kubectl patch sts mongo -p '{"spec": {"replicas": 0}}'
        echo "---"
        echo "Scaled down mongo STS on source."
        pod_down=$(date +%s%3N)
        pod_down_start_formatted=$(date '+%H:%M:%S.%3N')

	#change this later!
        #get pvc for destination
        kubectl get pvc mongo-pvc -o yaml | yq 'del(.metadata.uid, .metadata.resourceVersion, .metadata.annotations, .metadata.finalizers, .status)' > /tmp/pvc-mongo-tmp.yaml
	echo "---"
        echo "Get source PVC yaml."

        #also change later
        #get pv for dest
        kubectl get pv $(yq '.spec.volumeName' /tmp/pvc-mongo-tmp.yaml) -o yaml | yq 'del(.metadata.uid, .metadata.resourceVersion, .metadata.annotations, .metadata.finalizers, .spec.claimRef, .status)' > /tmp/pv-mongo-tmp.yaml
	echo "---"
        echo "Get source PV yaml."
        echo "---"

        #change cluster
        determine_dest_cluster
        kubectl config use-context $DEST_CLUSTER

        #apply yamls in dest
        kubectl create -f /tmp/pv-mongo-tmp.yaml
        kubectl create -f /tmp/pvc-mongo-tmp.yaml
        echo "Applied both yamls in destination."
        echo "---"

	echo "Waiting for PVC and PV to be ready"
        kubectl get pvc mongo-pvc -o jsonpath='{.status.phase}' | grep -q "Bound"
        kubectl get pv mongo-pv -o jsonpath='{.status.phase}' | grep -q "Bound"
        echo "PVC and PV ready"
        
	#scale up sts in dest
        #kubectl patch sts redis -p '{"spec": {"ordinals": {"start": 1}, "replicas": 1}}'
        kubectl patch sts mongo -p '{"spec": {"replicas": 1}}'
        echo "---"
        echo "Scaled up mongo STS on destination."

        #wait for pod ready in dest
        echo "---"
        echo "Waiting for pod to be ready."
        #POD_NAME=$(kubectl get pods -o=jsonpath='{.items[0].metadata.name}')
        kubectl wait --for=condition=Ready pod/mongo-0
        start_time2=$(date +%s%3N)
        formatted_time2=$(date '+%H:%M:%S.%3N')
        echo "Pod ready at: $formatted_time2"

        echo "---"
        echo "Started Migration at: $formatted_time"
        echo "Finished Migration at: $formatted_time2"
        echo "---"

        # calculate and display the duration in milliseconds
        duration=$((start_time2 - start_time))
        echo "Migration Duration: $duration ms"
        echo "$duration" >> "data/migration_duration_mongo_kill_first.txt"

        # pod downtime
        downtime=$((start_time2 - pod_down))
        echo "Pod downtime: $downtime ms"
        echo "$downtime" >> "data/pod_downtime_mongo_kill_first.txt"
        echo "---"
        echo "Cleaning up source cluster $CLUSTER"
        kubectl config use-context $CLUSTER
        kubectl delete pvc mongo-pvc
        kubectl delete pv mongo-pv
        kubectl config use-context $DEST_CLUSTER

        echo "---"
        echo "Generating data on mongo"
        start_time_client=$(date +%s%3N)
        downtime_client=$((start_time_client - downtime_client))
        #echo "$downtime_client" >> "data/client_downtime_kill_first.txt"
        ./generate_load.sh &
        sleep 300
done
