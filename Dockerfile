FROM ubuntu:16.04

RUN mkdir /bank

COPY app /bank/app

WORKDIR /bank

ENV FLASK_APP run.py

RUN apt-get update && apt-get install -y python-pip
RUN apt-get install -y apt-transport-https

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 58712A2291FA4AD5
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.6.list


RUN apt-get update && apt-get install -y mongodb-org
RUN apt-get install -y redis-server


ENV FLASK_APP run.py

COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY run.py config.py boot.sh ./
RUN mkdir -p /data/db

EXPOSE 5000

RUN chmod +x boot.sh 

ENTRYPOINT ["./boot.sh"]
