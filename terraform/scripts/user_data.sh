#!/bin/bash

#############################################
# Logging
#############################################

exec > >(tee /var/log/user-data.log | logger -t user-data ) 2>&1

#############################################
# Strict Mode
#############################################

set -euxo pipefail

trap 'echo "FAILED at line $LINENO"' ERR

echo "Starting bootstrap..."

#############################################
# Update Packages
#############################################

apt-get update -y

#############################################
# Install Dependencies
#############################################

apt-get install -y \
  openjdk-17-jdk \
  python3-pip \
  docker.io \
  wget \
  unzip \
  tar \
  gzip \
  curl

echo "Dependencies installed"

#############################################
# Install Docker Compose
#############################################

curl -SL \
https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 \
-o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "Docker Compose installed"

#############################################
# Start Docker
#############################################

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

echo "Docker configured"

#############################################
# Create Install Directory
#############################################

mkdir -p /opt

cd /opt

#############################################
# Install Kafka
#############################################

echo "Installing Kafka..."

wget https://downloads.apache.org/kafka/3.9.2/kafka_2.13-3.9.2.tgz

tar -xzf kafka_2.13-3.9.2.tgz

mv kafka_2.13-3.9.2 kafka

rm kafka_2.13-3.9.2.tgz

echo "Kafka installed"

#############################################
# Install Spark
#############################################

echo "Installing Spark..."

wget https://downloads.apache.org/spark/spark-3.5.8/spark-3.5.8-bin-hadoop3.tgz

tar -xzf spark-3.5.8-bin-hadoop3.tgz

mv spark-3.5.8-bin-hadoop3 spark

rm spark-3.5.8-bin-hadoop3.tgz

echo "Spark installed"

#############################################
# Install Python Libraries
#############################################

pip3 install \
  pyspark \
  kafka-python \
  boto3 \
  pandas \
  requests

echo "Python libraries installed"

#############################################
# Create Environment File
#############################################

mkdir -p /home/ubuntu/smartcity360

cat <<EOF > /home/ubuntu/smartcity360/.env
OPENWEATHER_API_KEY=${openweather_api_key}
TOMTOM_API_KEY=${tomtom_api_key}
OPENAQ_API_KEY=${openaq_api_key}
EOF

chown ubuntu:ubuntu /home/ubuntu/smartcity360/.env

chmod 600 /home/ubuntu/smartcity360/.env

echo ".env file created"

#############################################
# Environment Variables
#############################################

cat <<EOF >> /etc/profile

export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export SPARK_HOME=/opt/spark
export KAFKA_HOME=/opt/kafka
export PATH=\$PATH:/opt/kafka/bin:/opt/spark/bin

EOF

echo "Environment variables configured"

#############################################
# Permissions
#############################################

chown -R ubuntu:ubuntu /opt/kafka
chown -R ubuntu:ubuntu /opt/spark

echo "Permissions updated"

#############################################
# Verification
#############################################

java -version

ls -lah /opt

#############################################
# Validation Checks
#############################################

docker --version

docker-compose --version

java -version

test -d /opt/kafka

test -d /opt/spark

test -f /home/ubuntu/smartcity360/.env

echo "All validation checks passed"

#############################################
# Completion Marker
#############################################

echo "Bootstrap completed successfully"

touch /home/ubuntu/bootstrap-complete