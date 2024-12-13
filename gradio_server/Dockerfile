# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY count_dino.py .

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]