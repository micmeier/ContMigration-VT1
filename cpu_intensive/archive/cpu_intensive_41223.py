import datetime
import os
import re

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

filename = 'prime_numbers.txt'

# Check if the file exists
if os.path.exists(filename):
    # If the file exists, load the last value from the file
    with open(filename, 'r') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-2]  # Get the last line containing the previous prime number
            matches = re.findall(r'\d+', last_line)
            if len(matches) >= 2:
                prime_count, n = map(int, matches[:2])
                n += 1  # Move to the next number
            else:
                prime_count, n = 0, 2
        else:
            prime_count, n = 0, 2
else:
    # If the file doesn't exist, start from the beginning
    prime_count = 0
    n = 2

start_time = datetime.datetime.now()

# Open the file in append mode
while True:
    with open(filename, 'w') as file:
        if is_prime(n):
            prime_count += 1
            current_time = datetime.datetime.now()
            time_passed = (current_time - start_time).total_seconds() * 1000
            # Write the prime number and timestamp to the file
            file.write(f"{n}")
            # Print the prime number and timestamp
            print(f"Prime Number Count: {prime_count} | Prime Number: {n} | Start Time: {start_time} | Current Time: {current_time} | Time Passed: {time_passed:.2f}ms ")
            print("---")
            # Check the file size
            file_size = os.path.getsize(filename)
            # If the file size is greater than 1GB, break the loop
            if file_size >= 1e9:  # 1e9 bytes = 1GB
                print("The file size has reached 1GB. Stopping the script.")
                break
        n += 1
