#!/bin/bash

source ~/apps/utils/detector.sh

detect_cluster redis
detect_node redis 
detect_port redis

echo "Executing 'python3 data_generator.py $NODE $PORT'"
python3 data_generator.py $NODE $PORT
