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
            checkpointed.append(datetime.fromisoformat(row['Checkpointed']))
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

    # Calculate statistics for each metric
    metrics = {
        'Freezing Time': freezing_time,
        'Frozen Time': frozen_time,
        'Memdump Time': memdump_time,
        'Memwrite Time': memwrite_time,
        'Total Dump Time': total_dump_time
    }

    for metric, data in metrics.items():
        average = sum(data) / len(data)
        maximum = max(data)
        minimum = min(data)

        print(f"\n{metric} Statistics:")
        print(f"Average: {average} ms")
        print(f"Maximum: {maximum} ms")
        print(f"Minimum: {minimum} ms")

        # Plot metric over time
        plt.plot(checkpointed, data, marker='o', linestyle='-')
        plt.title(f'{metric} Over Time')
        plt.xlabel('Checkpoint Time')
        plt.ylabel(f'{metric} (ms)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 process_csv.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    process_csv(csv_file)
