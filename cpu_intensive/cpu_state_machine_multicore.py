import time
import multiprocessing
from multiprocessing import cpu_count
import subprocess
import os
import sys

#test git

# Define states
STATES = ['State 1', 'State 2', 'State 3', 'State 4']

def cpu_intensive_task():
    # Perform CPU int workload
    for _ in range(10**7):
        result = 2 ** 256

def cpu_intensive_worker(limit_percentage):
    # Set CPU limitation using cpulimit
    # subprocess.Popen() spawns a process that runs external cmds
    process = subprocess.Popen(['cpulimit', '-l', str(limit_percentage), '-p', str(os.getpid())])

    # Perform CPU-intensive tasks
    print("Performing CPU-intensive tasks...")
    cpu_intensive_task()

    # Terminate cpulimit subprocess
    process.terminate()

def main(limit_percentage, num_cores):
    # Start with State 1
    current_state_index = 0

    # Count cycles / Resembles "State"?
    cycle_count = 0

    # Init previous state index
    previous_state_index = len(STATES) - 1

    while True:
        current_state = STATES[current_state_index]

        print("---")
        print("The ParentPID of the current process is:", os.getpid())
        print(f"Current State: {current_state}")

        # Create a pool of processes
        pool = multiprocessing.Pool(processes=num_cores)

        # Execute the CPU-intensive worker function for each process
        pool.map(cpu_intensive_worker, [limit_percentage] * num_cores)

        # Transition to the next state
        next_state_index = (current_state_index + 1) % len(STATES)
        next_state = STATES[next_state_index]
        print(f"Transitioning to {next_state}")

        # Check transition from 4 to 1 for full cycle
        if current_state_index == 0 and previous_state_index == len(STATES) - 1:
                # Increment cycle count
                cycle_count += 1
                # print(f"Cycle Count incremented!")
                print(f"Current Cycle: {cycle_count}")

        # Update the current/previous state index
        previous_state_index = current_state_index
        current_state_index = next_state_index

if __name__ == "__main__":
    # Check if the CPU limit percentage and number of cores are provided as arguments
    if len(sys.argv) != 3:
        print("Usage: python3 .py <cpu_limit_percentage> <num_cores>")
        sys.exit(1)

    # Extract the CPU limit percentage and number of cores from the command-line arguments
    limit_percentage = int(sys.argv[1])
    num_cores = int(sys.argv[2])

    # Determine the number of CPU cores available
    num_cpus_available = cpu_count()

    if num_cores > num_cpus_available:
        print("Requested number of CPU cores exceeds available cores. Using all available cores.")
        num_cpus = num_cpus_available

    # Check if the CPU limit percentage is within the valid range (0-100)
    if not (0 <= limit_percentage <= 100):
        print("CPU limit percentage must be between 0 and 100")
        sys.exit(1)

    # Call the main function with the provided CPU limit percentage and number of cores
    main(limit_percentage, num_cores)
