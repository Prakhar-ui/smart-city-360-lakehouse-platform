import time
import requests

from datetime import datetime

from pydantic import BaseModel

from common.logger import logger

from common.kafka_client import (
    send_to_kafka
)

from common.config import (
    OPENAQ_API_KEY,
    CITY
)

TOPIC = "aqi_raw"

INTERVAL_SECONDS = 60

URL = (
    "https://api.openaq.org/v2/latest"
)

HEADERS = {
    "X-API-Key":
        OPENAQ_API_KEY
}

class AQISchema(BaseModel):

    city: str

    pm25: float

    pm10: float

    timestamp: datetime

def fetch_aqi_data():

    response = requests.get(
        URL,
        headers=HEADERS,
        params={"city": CITY},
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    measurements = (
        data["results"][0]
        ["measurements"]
    )

    pm25 = next(
        (
            item["value"]
            for item in measurements
            if item["parameter"]
            == "pm25"
        ),
        0
    )

    pm10 = next(
        (
            item["value"]
            for item in measurements
            if item["parameter"]
            == "pm10"
        ),
        0
    )

    return {

        "city": CITY,

        "pm25": pm25,

        "pm10": pm10,

        "timestamp":
            datetime.utcnow()
            .isoformat()
    }

def run():

    logger.info(
        "Starting AQI Producer"
    )

    while True:

        try:

            raw_data = (
                fetch_aqi_data()
            )

            validated_data = (
                AQISchema(
                    **raw_data
                ).model_dump()
            )

            send_to_kafka(
                TOPIC,
                validated_data
            )

            logger.info(
                f"AQI data sent: "
                f"{validated_data}"
            )

        except Exception as e:

            logger.error(
                f"AQI producer failed: "
                f"{e}"
            )

        time.sleep(
            INTERVAL_SECONDS
        )

if __name__ == "__main__":
    run()