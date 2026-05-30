#!/bin/bash

echo ""
echo "========================================"
echo "Smart City 360 Pipeline Status"
echo "========================================"

########################################
# ZooKeeper
########################################

echo ""
echo "ZooKeeper"

ps -ef | grep zookeeper | grep -v grep

########################################
# Kafka
########################################

echo ""
echo "Kafka Broker"

ps -ef | grep kafka.Kafka | grep -v grep

########################################
# Spark
########################################

echo ""
echo "Weather Stream"

ps -ef | grep weather_stream.py | grep -v grep

echo ""
echo "AQI Stream"

ps -ef | grep aqi_stream.py | grep -v grep

echo ""
echo "Traffic Stream"

ps -ef | grep traffic_stream.py | grep -v grep

########################################
# Docker
########################################

echo ""
echo "Producer Containers"

docker ps --format "table {{.Names}}\t{{.Status}}"

########################################
# Kafka Port
########################################

echo ""
echo "Kafka Port"

sudo ss -tulpn | grep 9092 || true

echo ""
echo "========================================"
echo "Status Check Complete"
echo "========================================"
echo ""