from pyspark.sql import SparkSession

from traffic_stream import (
    transform_traffic
)

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("test")
    .getOrCreate()
)

def test_traffic_transform():

    json_data = """

    {
        "city":"Bengaluru",
        "current_speed":20.0,
        "free_flow_speed":40.0,
        "congestion_percentage":50.0,
        "timestamp":"2026-01-01"
    }
    """

    df = spark.createDataFrame(
        [(json_data,)],
        ["value"]
    )

    result = (
        transform_traffic(df)
        .collect()
    )

    assert (
        result[0]["current_speed"]
        == 20.0
    )

    assert (
        result[0]["congestion_percentage"]
        == 50.0
    )