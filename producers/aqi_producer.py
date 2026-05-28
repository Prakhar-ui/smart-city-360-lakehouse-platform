import time
import requests

from datetime import datetime

from pydantic import BaseModel

from common.logger import logger

from common.kafka_client import (
    send_to_kafka
)

from common.config import (
    OPENWEATHER_API_KEY,
    CITY,
    LATITUDE,
    LONGITUDE
)

TOPIC = "aqi_raw"

INTERVAL_SECONDS = 60

URL = (
    "http://api.openweathermap.org/"
    "data/2.5/air_pollution"
)

class AQISchema(BaseModel):

    city: str

    aqi: int

    pm25: float

    pm10: float

    timestamp: datetime

def fetch_aqi_data():

    params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(
        URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()["list"][0]

    return {

        "city": CITY,

        "aqi":
            data["main"]["aqi"],

        "pm25":
            data["components"]["pm2_5"],

        "pm10":
            data["components"]["pm10"],

        "timestamp":
            datetime.utcnow().isoformat()
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
                ).model_dump(mode="json")
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