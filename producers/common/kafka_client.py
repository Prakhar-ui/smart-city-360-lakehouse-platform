import json

from confluent_kafka import Producer

from common.config import (
    KAFKA_BOOTSTRAP_SERVERS
)

producer = Producer({
    "bootstrap.servers":
        KAFKA_BOOTSTRAP_SERVERS
})

def delivery_report(err, msg):

    if err is not None:

        print(
            f"Delivery failed: {err}"
        )

    else:

        print(
            f"Delivered to "
            f"{msg.topic()} "
            f"[{msg.partition()}]"
        )

def send_to_kafka(topic, payload):

    producer.produce(
        topic,
        json.dumps(payload).encode("utf-8"),
        callback=delivery_report
    )

    producer.flush()