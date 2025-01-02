import time
import psutil

# Initialize the disk I/O stats counters
disk_stats = psutil.disk_io_counters()

# Loop every 10 seconds and print the stats
while True:
    time.sleep(5)
    disk_stats = psutil.disk_io_counters()
    print(f"Disk reads: {disk_stats.read_bytes}, Disk writes: {disk_stats.write_bytes}")
