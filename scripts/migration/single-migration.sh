#!/bin/bash
forensicAnalysis=false

# Parse command-line options
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -fa|--forensic-analysis) forensicAnalysis=true ;;
        -h|--help) echo "-- Usage: $0 <podName> [--forensic-analysis|-fa] --"; exit 0 ;;
        *) podName=$1 ;;
    esac
    shift
done

if [ -z "$podName" ]; then
    echo "-- Usage: $0 <podName> [--forensic-analysis|-fa] --"
    exit 1
fi

index=1
kubectl config use-context cluster1 || handle_error "Failed to switch context to cluster1"
appName=$(kubectl get pods $podName -o jsonpath='{.metadata.labels.app}') || handle_error "Failed to get app name"

log_dir="/home/ubuntu/contMigration_logs/$appName/$podName"
log_file="$log_dir/migration_log.txt"

# Create log directory and file if they do not exist
mkdir -p "$log_dir" || handle_error "Failed to create log directory"
touch "$log_file" || handle_error "Failed to create log file"

# Function to log messages
log() {
    echo "$1" >> "$log_file"
}

# Function to handle errors
handle_error() {
    log "Error: $1"
    exit 1
}



echo "Index, Checkpoint Creation, Checkpoint Location, Permission Change, Image Creation, Image Push, Pod Ready, Total" >> /home/ubuntu/meierm78/ContMigration-VT1/scripts/utils/data_extraction/data_dump/${podName}_migration_times.csv



log "Starting migration for $podName"

currentCluster=$(kubectl config current-context) || handle_error "Failed to get current context"
log "Source cluster: $currentCluster"

destCluster="cluster2"
log "Target cluster: $destCluster"

# Step 2: Get pod, container names, and node where the pod is running
containerName=$(kubectl get pods $podName -o jsonpath='{.spec.containers[0].name}') || handle_error "Failed to get container name"
nodename=$(kubectl get pods $podName -o jsonpath='{.spec.nodeName}') || handle_error "Failed to get node name"
# Step 3: Checkpoint via curl

log "-- Creating checkpoint for $podName on $nodename --"

migrationStartTime=$(date +%s%3N)

startTime=$(date +%s%3N)
checkpoint_output= curl -sk -X POST "https://$nodename:10250/checkpoint/default/${podName}/${containerName}" \
  --key /home/ubuntu/.kube/pki/$currentCluster-apiserver-kubelet-client.key \
  --cacert /home/ubuntu/.kube/pki/$currentCluster-ca.crt \
  --cert /home/ubuntu/.kube/pki/$currentCluster-apiserver-kubelet-client.crt || handle_error "Failed to create checkpoint"
checkpointTime=$(($(date +%s%3N) - $startTime))
log "checkpoint output: $checkpoint_output"
log "-- Checkpoint created --"

log "------------------------------------------------------------------"

log "-- Determining latest checkpoint for ${podName} --"

startTime=$(date +%s%3N)
# Step 4: Get path to newest checkpoint file with node name incorporated
checkpointfile=$(ls -1t /home/ubuntu/nfs/checkpoints/${nodename}/checkpoint-${podName}_default-${containerName}-*.tar | head -n 1)
latestCheckpointTime=$(($(date +%s%3N) - $startTime))

log "-- Latest checkpoint found --"

log "------------------------------------------------------------------"

log "-- Changing permissions for checkpoint file --"

startTime=$(date +%s%3N)
# Step 4.5: Change permissions of the checkpoint file
sudo chmod a+rwx "$checkpointfile" || handle_error "Failed to change permissions of checkpoint file"
permissionTime=$(($(date +%s%3N) - $startTime))

log "-- Permissions changed --"

log "------------------------------------------------------------------"

checkpoint_image_name=$(kubectl get pod $podName -o jsonpath='{.spec.containers[0].image}') || handle_error "Failed to get image name"

log "-- Convert checkpoint into image --"

startTime=$(date +%s%3N)
# Step 5: Convert checkpoint to image
log "Checkpoint image name: $checkpoint_image_name"
log "Checkpoint file: $checkpointfile"
newcontainer=$(buildah from $checkpoint_image_name) || handle_error "Failed to create new container"
buildah add $newcontainer $checkpointfile / || handle_error "Failed to add checkpoint file to container"
buildah config --annotation=io.kubernetes.cri-o.annotations.checkpoint.name=${containerName} $newcontainer || handle_error "Failed to add annotation to container"
newImageTime=$(($(date +%s%3N) - $startTime))

checkpoint_image_name=$(kubectl get pod $podName -o jsonpath='{.spec.containers[0].image}' | cut -d'/' -f 2 | cut -d':' -f 1) || handle_error "Failed to get image name"
log "Checkpoint image name: $checkpoint_image_name"
log "-- Commiting new image --"

startTime=$(date +%s%3N)
#sudo buildah commit $newcontainer $checkpoint_image_name:checkpoint
buildah commit $newcontainer $checkpoint_image_name:checkpoint || handle_error "Failed to commit new image"
buildah rm $newcontainer || handle_error "Failed to remove new container"

log "-- Pushing image \"$checkpoint_image_name:checkpoint\" to local registry --"
# Step 6: Push the image to local registry
buildah push --tls-verify=false localhost/$checkpoint_image_name:checkpoint 10.0.0.180:5000/$checkpoint_image_name:checkpoint || handle_error "Failed to push image to local registry"
pushImageTime=$(($(date +%s%3N) - $startTime))

log "-- Image pushed onto local registy --"

log "------------------------------------------------------------------"

# Step 9: Apply the updated YAML file
kubectl config use-context $destCluster || handle_error "Failed to switch context to $destCluster"

log "-- Applying restore yaml file --"

startTime=$(date +%s%3N)
kubectl apply -f /home/ubuntu/meierm78/ContMigration-VT1/scripts/migration/yaml/restore_$appName.yaml || handle_error "Failed to apply restore yaml file"

newPodName=$appName-restore

log "-- Waiting for the new pod \"$newPodName\" to be ready --"
kubectl wait --for=jsonpath='{.status.phase}'=Running pod/$newPodName || handle_error "Pod is not running"
podReadyTime=$(($(date +%s%3N) - $startTime))

migrationTotalTime=$(($(date +%s%3N) - $migrationStartTime))

echo "${index}, ${checkpointTime}, ${latestCheckpointTime}, ${permissionTime}, ${newImageTime}, ${pushImageTime}, ${podReadyTime}, ${migrationTotalTime}" >> /home/ubuntu/meierm78/ContMigration-VT1/scripts/utils/data_extraction/data_dump/${podName}_migration_times.csv

log "-- $newPodName running --"

log "------------------------------------------------------------------"

log "--- Deleting old pod ---"

kubectl config use-context cluster1 || handle_error "Failed to switch context to cluster1"
kubectl delete pod $podName || handle_error "Failed to delete pod"

sleep 5

log "-- Collecting checkpoint data --"
mkdir -p "/home/ubuntu/contMigration_logs/$appName/$podName"
/home/ubuntu/meierm78/ContMigration-VT1/scripts/utils/data_extraction/extract_info_with_output.sh $checkpointfile $index "/home/ubuntu/contMigration_logs/$appName/$podName"
log "-- Checkpoint data collected --"

log "------------------------------------------------------------------"

if [ "$forensicAnalysis" == true ]; then
  log "-- Performing forensic analysis --"
  sudo chmod 770 /home/ubuntu/meierm78/ContMigration-VT1/scripts/utils/forensic_analysis/forensic_analysis.sh
  /home/ubuntu/meierm78/ContMigration-VT1/scripts/utils/forensic_analysis/forensic_analysis.sh "$checkpointfile" "/home/ubuntu/contMigration_logs/$appName/$podName"
  log "-- Forensic analysis complete --"
fi

checkpointDir="/home/ubuntu/nfs/checkpoints/${nodename}/checkpoint-*_default-${containerName}-*.tar"
log "-- Deleting oldest checkpoint if more than 5 are saved --"

if  [ $(ls $checkpointDir | wc -l) -gt 5 ]
      then
  log "-- More than 5 checkpoint files for $podName on $nodename detected. Deleting oldest one... --"
  deleteFile=$(ls -1t $checkpointDir | tail -n 1)
  log "-- Deleting $deleteFile --"
  rm $(ls -1t $checkpointDir | tail -n 1)
else
  log "-- 5 or less checkpoint files for $podName on $nodename detected --"
fi

log "------------------------------------------------------------------"
log "-- Migration complete --"

exit 0
