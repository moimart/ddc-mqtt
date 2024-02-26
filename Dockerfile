# Use an official Python runtime as a parent image
FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libddcutil-dev \
    libddcutil4 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Build the extension module
RUN (cd simpleddc-extension && python setup.py build_ext --inplace)

# Install Python dependencies for the ddc-mqtt project
RUN pip install --no-cache-dir -r ./ddc-mqtt/requirements.txt

# Ensure the built module is available to the project
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/simpleddc"

# Change the working directory to run the ddc-mqtt project
WORKDIR /usr/src/app/ddc-mqtt

# Run start.py when the container launches
CMD ["python", "start.py"]

