#!/bin/bash

echo "========================================"
echo "Stopping Smart City 360 Pipeline"
echo "========================================"

########################################
# Spark Streams
########################################

echo "Stopping Spark Streams..."

pkill -f weather_stream.py || true

pkill -f aqi_stream.py || true

pkill -f traffic_stream.py || true

########################################
# Producers
########################################

echo "Stopping Producers..."

cd /home/ubuntu/smart-city-360-lakehouse-platform/producers

docker-compose down

########################################
# Kafka Broker
########################################

echo "Stopping Kafka..."

pkill -f kafka.Kafka || true

########################################
# ZooKeeper
########################################

echo "Stopping ZooKeeper..."

pkill -f QuorumPeerMain || true

echo ""
echo "Pipeline Stopped"
echo ""