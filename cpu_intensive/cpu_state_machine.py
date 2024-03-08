import time
import subprocess
import os
import sys

# Define states
STATES = ['State 1', 'State 2', 'State 3', 'State 4']

# Define transition times between states (in seconds)
TRANSITION_TIMES = [5, 5, 5, 5]

def cpu_intensive_task():
    # Perform CPU int worload
    for _ in range(10**7):
        result = 2 ** 256

def main(limit_percentage):
    # Start with first state
    current_state_index = 0

    # Count Cycles
    cycle_count = 0

    while True:
        current_state = STATES[current_state_index]
        print("---")
        print(f"Current State: {current_state}")

        # Set CPU limitation using cpulimit
        # subprocess.Popen() spawns a process that runs external cmds
        process = subprocess.Popen(['cpulimit', '-l', str(limit_percentage), '-p', str(os.getpid())])

        # Perform CPU-intensive tasks for the current state
        print("Performing CPU-intensive tasks...")
        cpu_intensive_task()

        # Terminate cpulimit subprocess
        # TODO: maybe change this?
        process.terminate()
        
        # Increment cycle count
        cycle_count += 1
        print(f"Cycle Count: {cycle_count}")

        # Transition to the next state
        next_state_index = (current_state_index + 1) % len(STATES)
        next_state = STATES[next_state_index]
        print(f"Transitioning to {next_state}")

        # Sleep for some time
#        time.sleep(TRANSITION_TIMES[current_state_index])

        # Update the current state index
        current_state_index = next_state_index


if __name__ == "__main__":
    # Check if the CPU limit percentage is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <cpu_limit_percentage>")
        sys.exit(1)

    # Extract the CPU limit percentage from the command-line argument
    limit_percentage = int(sys.argv[1])

    # Check if the CPU limit percentage is within the valid range (0-100)
    if not (0 <= limit_percentage <= 100):
        print("CPU limit percentage must be between 0 and 100")
        sys.exit(1)

    # Call the main function with the provided CPU limit percentage
    main(limit_percentage)
