# Use an official Python runtime as a parent image
FROM python:3.6.3-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install dependencies via apt-get
RUN apt-get update
RUN apt-get install -y openssh-server net-tools grep curl

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the bash script setup.sh
# RUN /bin/bash -c "source /app/setup.sh"
RUN netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2}' > host.txt

# Create SSH keypair
RUN ssh-keygen -t rsa -N "" -f ssh.key

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]