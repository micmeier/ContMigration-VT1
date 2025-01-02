import os
import random

with open("/home/ubuntu/disk_rw_intensive/test.bin", "wb") as f:
    for i in range(1024 * 1024 * 1024):
        f.write(random.randbytes(1024))

with open("/home/ubuntu/disk_rw_intensive/test.bin", "rb") as f:
    lines = []
    for line in f:
        lines.append(line)

os.remove("/home/ubuntu/disk_rw_intensive/test.bin")
