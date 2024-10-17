detect_cluster(){
	kubectl config use-context cluster1
	echo "Looking for $1 in cluster 1."
	
	if kubectl get pod/$1-0 &> /dev/null; then
		CLUSTER="cluster1"
	else
		echo "$1 not found in cluster 1. Switching to cluster 2."
		kubectl config use-context cluster2
		if kubectl get pod/$1-0 &> /dev/null; then
			CLUSTER="cluster2"
		else
			echo "$1 not detected. Terminating."
			exit 1
		fi
	fi

	echo "$1 detected in $CLUSTER."
}

detect_node(){
	echo "Looking for $1 in worker nodes."
	NODE=$(kubectl get pod/$1-0 -o jsonpath='{.spec.nodeName}')
	echo "$1 on $NODE detected."
}

detect_port(){
	echo "Determinating port"
	PORT=$(kubectl get svc $1-service -o jsonpath='{.spec.ports[0].nodePort}')
	echo "Port $PORT determined."
}

determine_dest_cluster(){
	echo "Determinating destination cluster."

	if [[ $CLUSTER == "cluster1" ]]; then
		DEST_CLUSTER="cluster2"
	else
		DEST_CLUSTER="cluster1"

	fi

	echo "Destination is $DEST_CLUSTER."
}
