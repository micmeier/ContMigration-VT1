#!/bin/bash

if [ -z "$1" ]
then
	echo "-- Usage: $0 <podName> --"
        exit 1
fi

podName=$1
index=0

echo "Index, Checkpoint Creation, Checkpoint Location, Permission Change, Image Creation, Image Push, Pod Ready, Total" >> /home/ubuntu/ContMigration/utils/data_extraction/data_dump/${podName}_migration_times.csv


while [ true ]
do
	echo "------------------------------------------------------------------"
	echo "-- Starting new migration --"
	
	index=$((index + 1))

	kubectl config use-context cluster1

	currentCluster=$(kubectl config current-context)
	echo "-- Current cluster: $currentCluster --"

	destCluster="cluster2"


	# Step 2: Get pod, container names, and node where the pod is running
	containername=$(kubectl get pods $podName -o jsonpath='{.spec.containers[0].name}')
	nodename=$(kubectl get pods $podName -o jsonpath='{.spec.nodeName}')

	# Step 3: Checkpoint via curl
	
	echo "------------------------------------------------------------------"
	
	echo "-- Creating checkpoint for $podName on $nodename --"
	
	migrationStartTime=$(date +%s%3N)

	startTime=$(date +%s%3N)
	curl -sk -X POST "https://$nodename:10250/checkpoint/default/${podName}/${containername}" \
	  --key /home/ubuntu/.kube/pki/$currentCluster-apiserver-kubelet-client.key \
	  --cacert /home/ubuntu/.kube/pki/$currentCluster-ca.crt \
	  --cert /home/ubuntu/.kube/pki/$currentCluster-apiserver-kubelet-client.crt
	checkpointTime=$(($(date +%s%3N) - $startTime))
	
	echo "-- Checkpoint created --"

	echo "------------------------------------------------------------------"
	
	echo "-- Determining latest checkpoint for ${podName} --"

	startTime=$(date +%s%3N)
	# Step 4: Get path to newest checkpoint file with node name incorporated
	checkpointfile=$(ls -1t /home/ubuntu/nfs/checkpoints/${nodename}/checkpoint-${podName}_default-${containername}-*.tar | head -n 1)
	latestCheckpointTime=$(($(date +%s%3N) - $startTime))

	echo "-- Latest checkpoint found --"
	
	echo "------------------------------------------------------------------"

	echo "-- Changing permissions for checkpoint file --"
	
	startTime=$(date +%s%3N)
	# Step 4.5: Change permissions of the checkpoint file
	sudo chmod a+rwx $checkpointfile
	permissionTime=$(($(date +%s%3N) - $startTime))

	echo "-- Permissions changed --"

	echo "------------------------------------------------------------------"
	
	checkpoint_image_name=$(kubectl get pod $podName -o jsonpath='{.spec.containers[0].image}')

	echo "-- Building new image --"
	
	startTime=$(date +%s%3N)
	# Step 5: Convert checkpoint to image
	newcontainer=$(buildah from $checkpoint_image_name)
	buildah add $newcontainer $checkpointfile /
	buildah config --annotation=io.kubernetes.cri-o.annotations.checkpoint.name=${containername} $newcontainer
	newImageTime=$(($(date +%s%3N) - $startTime))

	checkpoint_image_name=$(kubectl get pod $podName -o jsonpath='{.spec.containers[0].image}' | cut -d'/' -f 2 | cut -d':' -f 1)

	echo "-- Commiting new image --"
	
	startTime=$(date +%s%3N)
	#sudo buildah commit $newcontainer $checkpoint_image_name:checkpoint
	buildah commit $newcontainer $checkpoint_image_name:checkpoint
	buildah rm $newcontainer

	echo "-- Pushing image \"$checkpoint_image_name:checkpoint\" to local registry --"
	# Step 6: Push the image to local registry
	buildah push --tls-verify=false localhost/$checkpoint_image_name:checkpoint 10.0.0.180:5000/$checkpoint_image_name:checkpoint
	pushImageTime=$(($(date +%s%3N) - $startTime))

	echo "-- Image pushed onto local registy --"

	echo "------------------------------------------------------------------"

	# Step 9: Apply the updated YAML file
	kubectl config use-context $destCluster
	
	echo "-- Applying restore yaml file --"

	startTime=$(date +%s%3N)
	kubectl apply -f /home/ubuntu/ContMigration/migration/yaml/restore_$podName.yaml

	newPodName=$(echo $podName | cut -d'-' -f1)
	newStsName=$newPodName-restore
	newPodName=$newPodName-restore-0

	echo "-- Waiting for the new pod \"$newPodName\" to be ready --"
	kubectl wait --for=jsonpath='{.status.phase}'=Running pod/$newPodName
	podReadyTime=$(($(date +%s%3N) - $startTime))

	migrationTotalTime=$(($(date +%s%3N) - $migrationStartTime))
	
	echo "${index}, ${checkpointTime}, ${latestCheckpointTime}, ${permissionTime}, ${newImageTime}, ${pushImageTime}, ${podReadyTime}, ${migrationTotalTime}" >> /home/ubuntu/ContMigration/utils/data_extraction/data_dump/${podName}_migration_times.csv

	echo "-- newPodName running --"
	
	echo "------------------------------------------------------------------"

	sleep 5

	echo "-- Collecting checkpoint data --"
	/home/ubuntu/ContMigration/utils/data_extraction/extract_info_with_output.sh $checkpointfile $index
	echo "-- Checkpoint data collected --"

	echo "------------------------------------------------------------------"

	checkpointDir=/home/ubuntu/nfs/checkpoints/${nodename}/checkpoint-${podName}_default-${containername}-*.tar 
	echo "-- Deleting oldest checkpoint if more than 5 are saved --"

	if  [ $(ls $checkpointDir | wc -l) -gt 5 ]
       	then 
		echo "-- More than 5 checkpoint files for $podName on $nodename detected. Deleting oldest one... --"		
		deleteFile=$(ls -1t $checkpointDir | tail -n 1)
		echo "-- Deleting $deleteFile --"
		rm $(ls -1t $checkpointDir | tail -n 1)
	else 
		echo "-- 5 or less checkpoint files for $podName on $nodename detected --"
	fi

	echo "------------------------------------------------------------------"

	echo "-- Waiting for $newPodName to be deleted... --"
	kubectl delete sts $newStsName
	
	kubectl wait --for=delete pod/$newPodName
	echo "-- $newPodName deleted --"

	echo "-- Deleting all dangling images from local podman registry --"
	podman rmi $(podman images -q --filter "dangling=true")
done
