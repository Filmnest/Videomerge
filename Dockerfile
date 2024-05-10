FROM ubuntu:latest

# Set working directory
WORKDIR /usr/src/mergebot

# Make the directory writable
RUN chmod 777 /usr/src/mergebot

# Update package lists and install necessary packages
RUN apt-get -y update && apt-get -y upgrade && \
    apt-get install -y python3 python3-pip git \
    p7zip-full p7zip-rar xz-utils wget curl pv jq \
    ffmpeg unzip neofetch mediainfo

# Copy requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Set permissions for start.sh
RUN chmod +x start.sh

# Define the command to run the application
CMD ["bash", "start.sh"]
