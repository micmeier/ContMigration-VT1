import os
import random

#filename = "/home/ubuntu/disk_rw_intensive/test.bin"

# Check if the file exists
if os.path.exists("./test.bin"):
    mode = "r+b"
else:
    mode = "w+b"

with open("./test.bin", mode) as f:
    # Write 1024 bytes of random data to the file
    if mode == "w+b":
        f.write(random.randbytes(1024))

    # Loop 1,073,741,824 times (1024 * 1024 * 1024)
    for i in range(1024 * 1024 * 1024):
        # Randomly decide whether to write or read from the file
        if random.choice([True, False]):
            # Write another 1024 bytes of random data to the file
            f.write(random.randbytes(1024))
            # Flush the buffer to ensure that the data is written to disk
            f.flush()
            # Ensure that the data is written to disk
            os.fsync(f.fileno())
        else:
            # Move the file pointer back to the beginning of the file
            f.seek(0)
            # Read each line in the file without doing anything with it
            for line in f:
                pass

# Remove the test.bin file
os.remove("./test.bin")
