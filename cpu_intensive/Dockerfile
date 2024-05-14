# Use a Python base image
FROM python:3.9

# Set the working directory
WORKDIR /cpu_intensive

# Copy Python scripts into the container
COPY cpu_state_machine_singlecore.py cpu_state_machine_singlecore.py
COPY cpu_state_machine_multicore.py cpu_state_machine_multicore.py

# Copy the cpulimit executable into the container (adjusted for worker node)
#COPY /usr/bin/cpulimit /usr/bin/cpulimit

# Set permissions if necessary
#RUN chmod +x /usr/bin/cpulimit

# Default command to run the multicore script with parameters 25 and 2
CMD ["python3", "cpu_state_machine_multicore.py", "25", "2"]
