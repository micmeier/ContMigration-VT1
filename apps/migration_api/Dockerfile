# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY migration.py ./migration.py

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "migration.py"]
