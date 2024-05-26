#!/bin/bash

while [ true ]

	echo "------------------------------------------------------------------"
	echo "Starting new migration"
	
do
	if [ -z "$1" ]
	then
		echo "Usage: $0 <podName>"
		exit 1
	fi

	podName=$1

	currentCluster=$(kubectl config current-context)
	echo "Current cluster: $currentCluster"

	if [ $currentCluster == "cluster1" ]
	then	
		destCluster="cluster2"
	else
		destCluster="cluster1"
	fi

	# Step 2: Get pod, container names, and node where the pod is running
	containername=$(kubectl get pods $podName -o jsonpath='{.spec.containers[0].name}')
	nodename=$(kubectl get pods $podName -o jsonpath='{.spec.nodeName}')

	# Step 3: Checkpoint via curl
	echo "Creating checkpoint for $podName on $nodename"
	curl -sk -X POST "https://$nodename:10250/checkpoint/default/${podName}/${containername}" \
	  --key /home/ubuntu/.kube/pki/$currentCluster-apiserver-kubelet-client.key \
	  --cacert /home/ubuntu/.kube/pki/$currentCluster-ca.crt \
	  --cert /home/ubuntu/.kube/pki/$currentCluster-apiserver-kubelet-client.crt

	echo "Determining latest checkpoint for ${podName}"
	# Step 4: Get path to newest checkpoint file with node name incorporated
	checkpointfile=$(ls -1t /home/ubuntu/nfs/checkpoints/${nodename}/checkpoint-${podName}_default-${containername}-*.tar | head -n 1)

	echo "Changing permissions for checkpoint file"
	# Step 4.5: Change permissions of the checkpoint file
	sudo chmod a+rwx $checkpointfile

	checkpoint_image_name=$(kubectl get pod $podName -o jsonpath='{.spec.containers[0].image}')

	echo "Building new image"
	# Step 5: Convert checkpoint to image
	newcontainer=$(buildah from $checkpoint_image_name)
	buildah add $newcontainer $checkpointfile /
	buildah config --annotation=io.kubernetes.cri-o.annotations.checkpoint.name=${containername} $newcontainer

	checkpoint_image_name=$(kubectl get pod $podName -o jsonpath='{.spec.containers[0].image}' | cut -d'/' -f 2 | cut -d':' -f 1)

	echo "Commiting new image"
	#sudo buildah commit $newcontainer $checkpoint_image_name:checkpoint
	buildah commit $newcontainer $checkpoint_image_name:checkpoint
	buildah rm $newcontainer

	echo "Pushing image to local registry"
	# Step 6: Push the image to local registry
	buildah push --tls-verify=false localhost/$checkpoint_image_name:checkpoint 10.0.0.180:5000/$checkpoint_image_name:checkpoint
	
	# Step 9: Apply the updated YAML file
	kubectl config use-context $destCluster
	kubectl apply -f /home/ubuntu/ContMigration/migration/yaml/restore_$podName.yaml

	newPodName=$(echo $podName | cut -d'-' -f1)
	newStsName=$newPodName-restore
	newPodName=$newPodName-restore-0

	echo "Waiting for the new pod \"$newPodName\" to be ready"
	kubectl wait --for=condition=Ready pod/$newPodName
	echo "$newPodName ready"
	
	sleep 5

	echo "Collecting checkpoint data"
	/home/ubuntu/ContMigration/utils/data_extraction/extract_info_with_output.sh $checkpointfile 

	checkpointDir=/home/ubuntu/nfs/checkpoints/${nodename}/checkpoint-${podName}_default-${containername}-*.tar 
	echo "Deleting oldest checkpoint if more than 5 are saved"
	if  [ $(ls $checkpointDir | wc -l) -gt 5 ]
       	then 
		echo "More than 5 checkpoint files for $podName on $nodename detected. Deleting oldest one..."		
		deleteFile=$(ls -1t $checkpointDir | tail -n 1)
		echo "Deleting $deleteFile"
		rm $(ls -1t $checkpointDir | tail -n 1)
	else 
		echo "5 or less checkpoint files for $podName on $nodename detected."
	fi

	echo "Waiting for $newPodName to be deleted..."
	kubectl delete sts $newStsName
	
	kubectl wait --for=delete pod/$newPodName
	echo "$newPodName deleted"
done



