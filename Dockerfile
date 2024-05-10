FROM ubuntu:latest

# Set working directory
WORKDIR /usr/src/mergebot

# Make the directory writable
RUN chmod 777 /usr/src/mergebot

# Update package lists and install necessary packages
RUN apt-get -y update && apt-get -y upgrade && \
    apt-get install -y python3 python3-pip git \
    p7zip-full p7zip-rar xz-utils wget curl pv jq \
    ffmpeg unzip neofetch mediainfo python3-venv
