# Dockerfile
FROM python:3.12-slim

# Set the working directory
WORKDIR /app
COPY /LSManagement /app
# Copy the requirements file into the container


RUN pip install --upgrade pip
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run any Python script provided as an argument
WORKDIR /app/Webstuff
ENTRYPOINT ["python"]