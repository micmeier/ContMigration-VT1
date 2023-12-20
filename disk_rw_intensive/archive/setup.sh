#!/bin/bash

kubectl apply -f discrw.yaml

#test, Tony, copy prepared script into container/pod
kubectl cp /home/ubuntu/apps/disk_rw_intensive/mongodb_script_test.sh mongo-0:/mongodb_script_test.sh

kubectl exec -it mongo-0 -- /bin/sh mongodb_script_test.sh
