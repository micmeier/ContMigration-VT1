#!/bin/bash

kubectl delete sts mongo

kubectl delete svc mongo-service

kubectl delete pvc mongo-pvc

kubectl delete pv mongo-db
