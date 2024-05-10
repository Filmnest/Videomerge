FROM ubuntu:latest

WORKDIR /usr/src/mergebot
RUN chmod 777 /usr/src/mergebot

RUN apt-get -y update && apt-get -y upgrade && apt-get install apt-utils -y && \
    apt-get install -y python3 python3-pip git \
    p7zip-full p7zip-rar xz-utils wget curl pv jq \
    ffmpeg unzip neofetch mediainfo python3-venv

COPY requirements.txt .
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

CMD ["bash","start.sh"]
