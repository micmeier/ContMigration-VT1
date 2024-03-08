#!/bin/bash


read -p "How much Singlecore CPU Usage in percent? (Enter int between 1 and 100): " percent 

cpulimit -l $percent python3 cpu_state_machine_singlecore.py
