import time
import os
import sys
import psutil
from multiprocessing import Pool, cpu_count

# Define states
STATES = ['State 1', 'State 2', 'State 3', 'State 4']

def cpu_intensive_task():
    # Perform CPU int workload
    for _ in range(10**7):
        result = 2 ** 256

def perform_tasks(state):
    print("---")
    print("The PID of the current process is:", os.getpid())
    print(f"Current State: {state}")
    # Perform CPU-intensive tasks for the current state
    print("Performing CPU-intensive tasks...")
    cpu_intensive_task()

def main(cpu_limit_percentage, num_cpus):
    # Start with State 1
    current_state_index = 0

    # Count Cycles / Resembles "State"?
    cycle_count = 0

    # Init previous state index
    previous_state_index = len(STATES) - 1

    # Create a process pool with limited CPU usage
    with Pool(processes=num_cpus) as pool:
        while True:
            current_state = STATES[current_state_index]

            # Apply CPU limit to each process in the pool
            for process in psutil.Process().children(recursive=True):
                process.cpu_affinity([0])  # Restrict process to the first CPU core
                process.cpu_percent(cpu_limit_percentage)  # Limit CPU usage percentage

            # Execute tasks asynchronously
            pool.map(perform_tasks, STATES)

            # Transition to the next state
            next_state_index = (current_state_index + 1) % len(STATES)
            next_state = STATES[next_state_index]
            print(f"Transitioning to {next_state}")

            # Check transition from 4 to 1 for full cycle
            if current_state_index == 0 and previous_state_index == len(STATES) - 1:
                # Increment cycle count
                cycle_count += 1
                print(f"Current Cycle: {cycle_count}")

            # Update the current/previous state index
            previous_state_index = current_state_index
            current_state_index = next_state_index

if __name__ == "__main__":
    # Parse command-line arguments for CPU limit and number of CPU cores
    if len(sys.argv) >= 3:
        try:
            cpu_limit_percentage = float(sys.argv[1])
            num_cpus = int(sys.argv[2])
        except ValueError:
            print("Invalid arguments. Please provide CPU limit percentage and number of CPU cores.")
            sys.exit(1)
    else:
        print("Usage: python3 script.py <cpu_limit_percentage> <num_cpus>")
        sys.exit(1)

    # Determine the number of CPU cores available
    num_cpus_available = cpu_count()

    if num_cpus > num_cpus_available:
        print("Requested number of CPU cores exceeds available cores. Using all available cores.")
        num_cpus = num_cpus_available

    print(f"Using {num_cpus} CPU core(s) out of {num_cpus_available} available core(s).")
    print(f"CPU limit percentage: {cpu_limit_percentage}%")

    # Call the main function
    main(cpu_limit_percentage, num_cpus)
