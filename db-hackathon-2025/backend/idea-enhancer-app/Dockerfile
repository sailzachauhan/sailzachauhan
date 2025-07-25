# Use the official Python image as a base
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
# This allows Docker to cache the layer if requirements don't change
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port that your Flask app will listen on
# Cloud Run injects the PORT environment variable, so use it.
ENV PORT 8080
EXPOSE $PORT
# Expose the port from the environment variable
EXPOSE 8080

# Command to run the application using Gunicorn
# 'app:app' means the 'app' variable from the 'app.py' file.
# The bind address and port are specified here.
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 app:app