from pyspark.sql import SparkSession

from spark.weather_stream import (
    transform_weather
)

spark = (

    SparkSession.builder

    .master("local[*]")

    .appName("test")

    .getOrCreate()
)

def test_weather_transform():

    json_data = """

    {
        "city":"Bengaluru",
        "temperature":30.5,
        "humidity":70,
        "pressure":1000,
        "weather_condition":"Clouds",
        "wind_speed":3.2,
        "timestamp":"2026-01-01"
    }
    """

    df = spark.createDataFrame(
        [(json_data,)],
        ["value"]
    )

    result = (
        transform_weather(df)
        .collect()
    )

    assert (
        result[0]["city"]
        == "Bengaluru"
    )

    assert (
        result[0]["temperature"]
        == 30.5
    )