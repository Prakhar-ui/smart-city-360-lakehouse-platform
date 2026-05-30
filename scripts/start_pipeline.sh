#!/bin/bash

set -e

echo "========================================"
echo "Starting Smart City 360 Pipeline"
echo "========================================"

########################################
# ZooKeeper
########################################

echo "Starting ZooKeeper..."

cd /opt/kafka

nohup bin/zookeeper-server-start.sh \
config/zookeeper.properties \
> /home/ubuntu/zookeeper.log 2>&1 &

sleep 10

########################################
# Kafka Broker
########################################

echo "Starting Kafka Broker..."

nohup bin/kafka-server-start.sh \
config/server.properties \
> /home/ubuntu/kafka.log 2>&1 &

sleep 15

########################################
# Verify Kafka
########################################

echo "Verifying Kafka..."

bin/kafka-topics.sh \
--list \
--bootstrap-server localhost:9092

########################################
# Producers
########################################

echo "Starting Producers..."

cd /home/ubuntu/smart-city-360-lakehouse-platform/producers

docker-compose up -d

sleep 10

########################################
# Spark Streams
########################################

echo "Starting Weather Stream..."

cd /home/ubuntu/smart-city-360-lakehouse-platform/spark

nohup spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
weather_stream.py \
> /home/ubuntu/weather_stream.log 2>&1 &

sleep 5

echo "Starting AQI Stream..."

nohup spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
aqi_stream.py \
> /home/ubuntu/aqi_stream.log 2>&1 &

sleep 5

echo "Starting Traffic Stream..."

nohup spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
traffic_stream.py \
> /home/ubuntu/traffic_stream.log 2>&1 &

sleep 5

echo ""
echo "Pipeline Started Successfully"
echo ""