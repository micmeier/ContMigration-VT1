#!/bin/bash

num_cores=$(nproc)

echo "$num_cores CPU cores available."

read -p "How many cores should be utilized? Available: Choose between 1-$num_cores: " chosen_cores

echo "You chose $chosen_cores cores."

read -p "How much CPU Usage per core in percent? (Enter int between 1 and 100): " chosen_percentage 

if [ "$chosen_cores" -eq 1 ]; then
	cpulimit -l $chosen_percentage python3 cpu_state_machine_singlecore.py
else
	python3 cpu_state_machine_multicore.py $chosen_percentage $chosen_cores &
fi
