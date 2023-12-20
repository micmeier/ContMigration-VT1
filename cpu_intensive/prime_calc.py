import datetime
import os
import re
import time

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

filename = 'state_cpu.txt'

# Check if the file exists
if os.path.exists(filename):
    # If the file exists, load the last value from the file
    with open(filename, 'r') as file:
        n = int(file.read().strip())
        
else:
    n = 2

start_time = datetime.datetime.now()

# Open the file in append mode
while True:     
    f = open(filename, 'w') 
    f.write(f"{n}")
    f.close()

    if is_prime(n):
        current_time = datetime.datetime.now()
        time_passed = (current_time - start_time).total_seconds() * 1000
        print(f"Prime Number: {n} | Start Time: {start_time} | Current Time: {current_time} | Time Passed: {time_passed:.2f}ms")    
    
    n += 1

# using 0.1 out to test
    time.sleep(0.001)
