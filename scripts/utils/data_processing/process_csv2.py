import sys
import csv
import matplotlib.pyplot as plt
from datetime import datetime

def process_csv(csv_file):
    # Initialize lists to store data
    checkpointed = []
    freezing_time = []
    frozen_time = []
    memdump_time = []
    memwrite_time = []
    total_dump_time = []

    # Read the CSV file and extract relevant data
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            checkpointed_str = row['Checkpointed'].rstrip('Z')
            checkpointed.append(datetime.fromisoformat(checkpointed_str))
            freezing_time_str = row['Freezing time']
            freezing_time_ms = float(freezing_time_str.split()[0])
            if 'µs' in freezing_time_str:
                # Convert microseconds to milliseconds
                freezing_time_ms /= 1000
            freezing_time.append(freezing_time_ms)
            frozen_time.append(float(row['Frozen time'].split()[0]))
            memdump_time.append(float(row['Memdump time'].split()[0]))
            memwrite_time.append(float(row['Memwrite time'].split()[0]))
            total_dump_time.append(float(row['Total dump time (ms)']))

    # Combine lists into a list of tuples and sort by checkpointed time
    combined_data = list(zip(checkpointed, freezing_time, frozen_time, memdump_time, memwrite_time, total_dump_time))
    combined_data.sort(key=lambda x: x[0])  # Sort by the first element of the tuple (checkpointed time)

    # Unzip the sorted data
    checkpointed, freezing_time, frozen_time, memdump_time, memwrite_time, total_dump_time = zip(*combined_data)

    # Calculate statistics for each metric
    metrics = {
        'Freezing Time': freezing_time,
        'Frozen Time': frozen_time,
        'Memdump Time': memdump_time,
        'Memwrite Time': memwrite_time,
        'Total Dump Time': total_dump_time
    }

    averages = []
    maximums = []
    minimums = []

    for metric, data in metrics.items():
        average = sum(data) / len(data)
        maximum = max(data)
        minimum = min(data)

        averages.append(average)
        maximums.append(maximum)
        minimums.append(minimum)

        print(f"\n{metric} Statistics:")
        print(f"Average: {average} ms")
        print(f"Maximum: {maximum} ms")
        print(f"Minimum: {minimum} ms")

        # Plot metric over time
        plt.figure(figsize=(10, 6))  # Increase figure size for better readability
        plt.plot(checkpointed, data, marker='o', linestyle='-')
        plt.title(f'{metric} Over Time')
        plt.xlabel('Checkpoint Time')
        plt.ylabel(f'{metric} (ms)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Determine y-axis limits with more padding for better separation
    y_min = 0  # Start y-axis from zero
    y_max = max(max(maximums) * 1.1, 120)  # Add 10% padding to the top

    # Plot summary of averages, minimums, and maximums for each metric
    metrics_names = list(metrics.keys())
    x = range(len(metrics_names))

    plt.figure(figsize=(12, 8))
    plt.plot(metrics_names, averages, marker='o', linestyle='-', label='Average')
    plt.plot(metrics_names, minimums, marker='o', linestyle='-', label='Minimum')
    plt.plot(metrics_names, maximums, marker='o', linestyle='-', label='Maximum')

    plt.xticks(rotation=45)
    plt.xlabel('Metrics')
    plt.ylabel('Time (ms)')
    plt.title('Summary of Metrics')
    plt.ylim(y_min, y_max)  # Set y-axis limits with padding
    plt.yticks(range(0, int(y_max) + 10, 10))
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 process_csv.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    process_csv(csv_file)
