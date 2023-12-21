import matplotlib.pyplot as plt
import numpy as np
import sys

def process_file(file_path):
    with open(file_path, 'r') as file:
        data = [int(line.strip()) for line in file]

    # Sort the data
    data.sort()

    # Calculate iterations and basic statistics
    iterations = len(data)
    average_ms = np.mean(data)
    median_ms = np.median(data)
    std_dev_ms = np.std(data)
    min_duration = np.min(data)
    max_duration = np.max(data)

    # Append "sorted" to the output filename
    output_filename = f'{file_path}_sorted'

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(data, marker='o', label=f'{output_filename} ({iterations} iterations)')
    plt.xlabel('Iteration')
    plt.ylabel('Duration (ms)')
    plt.axhline(y=average_ms, color='r', linestyle='--', label=f'Average ({average_ms:.2f} ms)')
    plt.axhline(y=median_ms, color='g', linestyle='--', label=f'Median ({median_ms} ms)')
    plt.axhline(y=std_dev_ms, color='b', linestyle='--', label=f'Standard Deviation ({std_dev_ms:.2f} ms)')
    plt.axhline(y=min_duration, color='y', linestyle='--', label=f'Minimum ({min_duration} ms)')
    plt.axhline(y=max_duration, color='purple', linestyle='--', label=f'Maximum ({max_duration} ms)')
    plt.fill_between(range(iterations), average_ms - std_dev_ms, average_ms + std_dev_ms, color='gray', alpha=0.3, label='1 SD Range')

    # Move the legend to the top of the plot
    plt.legend(bbox_to_anchor=(0.5, 1.15), loc='upper center', ncol=3)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{output_filename}_plot.png', bbox_inches='tight')
    plt.show()


file_path = "C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/mem_intensive/data/migration_duration_kill_first.txt"
process_file(file_path)

