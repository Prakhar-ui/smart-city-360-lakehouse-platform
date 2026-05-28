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
    CITY
)

TOPIC = "weather_raw"

INTERVAL_SECONDS = 60

URL = (
    "https://api.openweathermap.org/"
    "data/2.5/weather"
)

class WeatherSchema(BaseModel):

    city: str

    temperature: float

    humidity: int

    pressure: int

    weather_condition: str

    wind_speed: float

    timestamp: datetime

def fetch_weather_data():

    params = {
        "q": CITY,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(
        URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return {

        "city": CITY,

        "temperature":
            data["main"]["temp"],

        "humidity":
            data["main"]["humidity"],

        "pressure":
            data["main"]["pressure"],

        "weather_condition":
            data["weather"][0]["main"],

        "wind_speed":
            data["wind"]["speed"],

        "timestamp":
            datetime.utcnow().isoformat()
    }

def run():

    logger.info(
        "Starting Weather Producer"
    )

    while True:

        try:

            raw_data = (
                fetch_weather_data()
            )

            validated_data = (
                WeatherSchema(
                    **raw_data
                ).model_dump(mode="json")
            )

            send_to_kafka(
                TOPIC,
                validated_data
            )

            logger.info(
                f"Weather data sent: "
                f"{validated_data}"
            )

        except Exception as e:

            logger.error(
                f"Weather producer failed: "
                f"{e}"
            )

        time.sleep(
            INTERVAL_SECONDS
        )

if __name__ == "__main__":
    run()