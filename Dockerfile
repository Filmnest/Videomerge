FROM heroku/heroku:18

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip git \
    p7zip-full p7zip-rar xz-utils wget curl pv jq \
    ffmpeg unzip neofetch mediainfo

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set permissions
RUN chmod +x start.sh

# Specify the command to run your application
CMD ["./start.sh"]

