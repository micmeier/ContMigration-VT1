import datetime
import os

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

n = 2
prime_count = 0
start_time = datetime.datetime.now()
filename = 'prime_numbers.txt'

# Open a file in write mode
with open(filename, 'w') as file:
    while True:
        if is_prime(n):
            prime_count += 1
            current_time = datetime.datetime.now()
            time_passed = (current_time - start_time).total_seconds() * 1000
            # Write the prime number and timestamp to the file
            file.write(f"Prime Number Count: {prime_count} | Prime Number: {n} | Start Time: {start_time} | Current Time: {current_time} | Time Passed: {time_passed:.2f}ms\n")
            file.write("---\n")
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
