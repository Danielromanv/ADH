FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python3 \
  && pip3 install --upgrade pip \
  && apt-get install nmap

WORKDIR /AutoABM
COPY /AutoABM/ /AutoABM/

RUN pip install -r requirements.txt
