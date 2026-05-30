#!/bin/bash

echo ""
echo "=================================="
echo "Smart City 360 Pipeline Status"
echo "=================================="

check_service() {

    SERVICE_NAME=$1
    PROCESS=$2

    if pgrep -f "$PROCESS" > /dev/null
    then
        echo "✅ $SERVICE_NAME : RUNNING"
    else
        echo "❌ $SERVICE_NAME : STOPPED"
    fi
}

check_container() {

    CONTAINER=$1

    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"
    then
        echo "✅ $CONTAINER : RUNNING"
    else
        echo "❌ $CONTAINER : STOPPED"
    fi
}

check_service "ZooKeeper" "QuorumPeerMain"

check_service "Kafka Broker" "kafka.Kafka"

check_container "weather-producer"

check_container "aqi-producer"

check_container "traffic-producer"

check_service "Weather Stream" "weather_stream.py"

check_service "AQI Stream" "aqi_stream.py"

check_service "Traffic Stream" "traffic_stream.py"

echo ""
echo "=================================="