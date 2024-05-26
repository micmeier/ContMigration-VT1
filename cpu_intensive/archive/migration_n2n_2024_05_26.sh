#!/bin/bash

read -p "Which pod do you want to restore? " podName

currentCluster=$(kubectl config current-context)
# Step 2: Get pod, container names, and node where the pod is running
#podname=$(kubectl get pods -o jsonpath='{.items[0].metadata.name}')
containername=$(kubectl get pods $podName -o jsonpath='{.spec.containers[0].name}')
nodename=$(kubectl get pods $podName -o jsonpath='{.spec.nodeName}')



# Step 3: Checkpoint via curl
echo "Creating checkpoint for $podName on $nodename"
curl -sk -X POST "https://${nodename}:10250/checkpoint/default/${podName}/${containername}" \
  --key /home/ubuntu/.kube/pki/$currentCluster-apiserver-kubelet-client.key \
  --cacert /home/ubuntu/.kube/pki/$currentCluster-ca.crt \
  --cert /home/ubuntu/.kube/pki/$currentCluster-apiserver-kubelet-client.crt
echo "Checkpoint created"

# Step 4: Get path to newest checkpoint file with node name incorporated
checkpointfile=$(ls -1t /home/ubuntu/nfs/checkpoints/${nodename}/checkpoint-${podName}_default-${containername}-*.tar | head -n 1)

#echo "Changing permissions of checkpointfile $checkpointfile"
# Step 4.5: Change permissions of the checkpoint file
sudo chmod a+rwx $checkpointfile

echo "Building new image"
# Step 5: Convert checkpoint to image
newcontainer=$(buildah from scratch)
buildah add $newcontainer $checkpointfile /
buildah config --annotation=io.kubernetes.cri-o.annotations.checkpoint.name=${containername} $newcontainer

# Define the checkpoint image name without :latest
checkpoint_image_name=$(kubectl get pod $podName -o jsonpath='{.spec.containers[0].image}' | cut -d'/' -f 2 | cut -d':' -f 1)
checkpoint_image_name="${checkpoint_image_name}restore"

#buildah commit $newcontainer $checkpoint_image_name:checkpoint
buildah commit $newcontainer $checkpoint_image_name:checkpoint
buildah rm $newcontainer

echo "Pushing new image into local registry"wq
# Step 6: Push the image to local registry
buildah push --tls-verify=false localhost/$checkpoint_image_name:checkpoint 10.0.0.180:5000/$checkpoint_image_name:checkpoint
echo "New image \"$checkpoint_image_name\" pushed to local registry"

# Step 7: Adjust image name in the restore YAML file
#sed -i "s|10.0.0.180:5000/localcpusinglecorerestore:checkpoint|10.0.0.180:5000/$checkpoint_image_name:checkpoint|g" yaml/restore_sts_cpu_singlecore.yaml

# Step 8: Adjust node name in the restore YAML file
#sed -i "s|nodeName: worker1|nodeName: $nodename|g" migr/restore_sts_cpu_singlecore.yaml

echo "Applying YAML file"
# Step 9: Apply the updated YAML file
kubectl apply -f yaml/test.yaml
#kubectl run webserver-restore --image 10.0.0.180:5000/nginxrestore:checkpoint

