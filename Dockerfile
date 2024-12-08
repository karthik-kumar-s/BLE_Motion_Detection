# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Python to run in non-buffered mode (helps with logs)
ENV PYTHONUNBUFFERED=1

# Command to run the app
CMD ["python", "ble_motion_detection.py"]
