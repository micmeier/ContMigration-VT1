import sys
import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Function to convert time strings to milliseconds
def convert_to_ms(time_str):
    if 'ms' in time_str:
        return float(time_str.split()[0])
    elif 'µs' in time_str:
        return float(time_str.split()[0]) / 1000
    return 0

# Function to plot checkpoint data
def plot_checkpoint_data(file_path):
    # Initialize lists to store the data
    checkpointed_times = []
    freezing_times = []
    frozen_times = []
    memdump_times = []
    memwrite_times = []
    total_dump_times = []

    # Read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            checkpointed_times.append(datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%SZ"))
            freezing_times.append(convert_to_ms(row[3]))
            frozen_times.append(convert_to_ms(row[4]))
            memdump_times.append(convert_to_ms(row[5]))
            memwrite_times.append(convert_to_ms(row[6]))
            total_dump_times.append(float(row[7]))

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(checkpointed_times, freezing_times, marker='o', label='Freezing time (ms)')
    plt.plot(checkpointed_times, frozen_times, marker='o', label='Frozen time (ms)')
    plt.plot(checkpointed_times, memdump_times, marker='o', label='Memdump time (ms)')
    plt.plot(checkpointed_times, memwrite_times, marker='o', label='Memwrite time (ms)')
    plt.plot(checkpointed_times, total_dump_times, marker='o', linestyle='--', label='Total dump time (ms)')

    plt.xlabel('Checkpointed Time')
    plt.ylabel('Time (ms)')
    plt.title('CRIU Dump Statistics Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("checkpoint_data_plot.png")


    # Show the plot
#    plt.show()

if __name__ == "__main__":
    # Check if the CSV file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python plot_checkpoint_data.py <csv_file>")
        sys.exit(1)

    # Get the CSV file path from command-line arguments
    csv_file = sys.argv[1]

    # Plot checkpoint data
    plot_checkpoint_data(csv_file)
