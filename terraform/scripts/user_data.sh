#!/bin/bash

exec > >(tee /var/log/user-data.log|logger -t user-data ) 2>&1

set -euxo pipefail

echo "Starting bootstrap..."

#############################################
# Update Packages
#############################################

apt-get update -y

#############################################
# Install Dependencies
#############################################

apt-get install -y \
  openjdk-11-jdk \
  python3-pip \
  docker.io \
  wget \
  unzip

#############################################
# Start Docker
#############################################

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

#############################################
# Create Install Directory
#############################################

mkdir -p /opt
cd /opt

#############################################
# Install Kafka
#############################################

wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz

tar -xzf kafka_2.13-3.7.0.tgz

mv kafka_2.13-3.7.0 kafka

rm kafka_2.13-3.7.0.tgz

#############################################
# Install Spark
#############################################

wget https://downloads.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz

tar -xzf spark-3.5.1-bin-hadoop3.tgz

mv spark-3.5.1-bin-hadoop3 spark

rm spark-3.5.1-bin-hadoop3.tgz

#############################################
# Install Python Libraries
#############################################

pip3 install \
  pyspark \
  kafka-python \
  boto3 \
  pandas \
  requests

#############################################
# Environment Variables
#############################################

cat <<EOF >> /etc/profile

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/opt/spark
export PATH=\$PATH:/opt/kafka/bin:/opt/spark/bin

EOF

#############################################
# Permissions
#############################################

chown -R ubuntu:ubuntu /opt/kafka
chown -R ubuntu:ubuntu /opt/spark

#############################################
# Completion Marker
#############################################

echo "Bootstrap completed successfully"

touch /home/ubuntu/bootstrap-complete