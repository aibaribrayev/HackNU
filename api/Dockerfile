# Start with a base image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /app

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the default port used by Django
EXPOSE 8000