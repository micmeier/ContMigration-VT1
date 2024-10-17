import time
import os
import sys

# Define states
STATES = ['State 1', 'State 2', 'State 3', 'State 4']

def cpu_intensive_task():
    # Perform CPU int workload
    for _ in range(10**7):
        result = 2 ** 256

def main():
    # Start with State 1
    current_state_index = 0

    # Count Cycles / Resembles "State" together with current_state_index
    cycle_count = 0

    # Init previous state index
    previous_state_index = len(STATES) - 1

    while True:
        current_state = STATES[current_state_index]

        print("---")
        print("The PID of the current process is:", os.getpid())
        print(f"Current State: {current_state}")

        # Perform CPU-intensive tasks for the current state
        print("Performing CPU-intensive tasks...")
        cpu_intensive_task()

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

    # Call the main function
    main()
