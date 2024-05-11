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

# Upgrade pip
RUN pip3 install -U pip

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
