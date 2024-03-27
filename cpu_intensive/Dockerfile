# Use a Python base image
FROM python:3.9

# Set the working directory
WORKDIR /cpu_intensive

# Copy Python scripts into the container
COPY cpu_state_machine_singlecore.py cpu_state_machine_singlecore.py
COPY cpu_state_machine_multicore.py cpu_state_machine_multicore.py

# Default command: Sleep indefinitely
#CMD ["sleep", "infinity"]
