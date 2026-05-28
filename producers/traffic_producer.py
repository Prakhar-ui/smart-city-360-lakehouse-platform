import time
import requests

from datetime import datetime

from pydantic import BaseModel

from common.logger import logger

from common.kafka_client import (
    send_to_kafka
)

from common.config import (
    TOMTOM_API_KEY,
    CITY,
    LATITUDE,
    LONGITUDE
)

TOPIC = "traffic_raw"

INTERVAL_SECONDS = 60

URL = (
    "https://api.tomtom.com/"
    "traffic/services/4/"
    "flowSegmentData/"
    "absolute/10/json"
)

class TrafficSchema(BaseModel):

    city: str

    current_speed: float

    free_flow_speed: float

    congestion_percentage: float

    timestamp: datetime

def fetch_traffic_data():

    params = {
        "key": TOMTOM_API_KEY,
        "point":
            f"{LATITUDE},"
            f"{LONGITUDE}"
    }

    response = requests.get(
        URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()[
        "flowSegmentData"
    ]

    current_speed = (
        data["currentSpeed"]
    )

    free_flow_speed = (
        data["freeFlowSpeed"]
    )

    congestion_percentage = round(

        (
            1 -
            (
                current_speed /
                free_flow_speed
            )
        ) * 100,

        2
    )

    return {

        "city": CITY,

        "current_speed":
            current_speed,

        "free_flow_speed":
            free_flow_speed,

        "congestion_percentage":
            congestion_percentage,

        "timestamp":
            datetime.utcnow().isoformat()
    }

def run():

    logger.info(
        "Starting Traffic Producer"
    )

    while True:

        try:

            raw_data = (
                fetch_traffic_data()
            )

            validated_data = (
                TrafficSchema(
                    **raw_data
                ).model_dump(mode="json")
            )

            send_to_kafka(
                TOPIC,
                validated_data
            )

            logger.info(
                f"Traffic data sent: "
                f"{validated_data}"
            )

        except Exception as e:

            logger.error(
                f"Traffic producer failed: "
                f"{e}"
            )

        time.sleep(
            INTERVAL_SECONDS
        )

if __name__ == "__main__":
    run()