#!/bin/bash

source ~/ContMigration/utils/detector.sh

detect_cluster mongo
detect_node mongo
detect_port mongo

echo "Executing 'python3 data_generator.py $NODE $PORT'"
python3 /home/ubuntu/ContMigration/disk_rw_intensive/python_scripts/data_generator.py $NODE $PORT
