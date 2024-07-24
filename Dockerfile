# Dockerfile
FROM python:3.12-slim

# Set the working directory
WORKDIR /app
COPY database /app/database/
COPY utils /app/utils/
COPY Webstuff /app/Webstuff/
# Copy the requirements file into the container
COPY requirements.txt /app/

RUN pip install --upgrade pip
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
# Command to run any Python script provided as an argument
WORKDIR /app/Webstuff
ENV FLASK_APP=Webstuff/app.py
ENTRYPOINT ["/bin/bash"]