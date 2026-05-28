import os

from dotenv import load_dotenv

load_dotenv("/home/ubuntu/smartcity360/.env")

# API KEYS

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)

OPENAQ_API_KEY = os.getenv(
    "OPENAQ_API_KEY"
)

TOMTOM_API_KEY = os.getenv(
    "TOMTOM_API_KEY"
)

# KAFKA

KAFKA_BOOTSTRAP_SERVERS = (
    "localhost:9092"
)

# CITY CONFIG

CITY = "Bengaluru"

LATITUDE = 12.9716

LONGITUDE = 77.5946