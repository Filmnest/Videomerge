FROM ubuntu:latest

# Update packages and install dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    p7zip-full \
    p7zip-rar \
    xz-utils \
    wget \
    curl \
    pv \
    jq \
    unzip \
    neofetch \
    mediainfo && \
    rm -rf /var/lib/apt/lists/*

# Install pip using get-pip.py script
RUN python3 -m ensurepip --default-pip && \
    python3 -m pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /usr/src/mergebot

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set permissions for start.sh
RUN chmod +x start.sh

# Run the application
CMD ["bash", "start.sh"]
