#!/bin/bash

apt-get update -y

apt-get install -y \
  openjdk-11-jdk \
  python3-pip \
  docker.io \
  wget \
  unzip

systemctl start docker
systemctl enable docker

# Kafka
cd /opt

wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz

tar -xzf kafka_2.13-3.7.0.tgz

mv kafka_2.13-3.7.0 kafka

# Spark
wget https://downloads.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz

tar -xzf spark-3.5.1-bin-hadoop3.tgz

mv spark-3.5.1-bin-hadoop3 spark

# Python Libraries
pip3 install \
  pyspark \
  kafka-python \
  boto3 \
  pandas \
  requests

echo "Bootstrap completed" > /home/ubuntu/setup.log