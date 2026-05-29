from pyspark.sql import SparkSession

from aqi_stream import (
    transform_aqi
)

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("test")
    .getOrCreate()
)

def test_aqi_transform():

    json_data = """

    {
        "city":"Bengaluru",
        "aqi":2,
        "pm25":15.0,
        "pm10":20.0,
        "timestamp":"2026-01-01"
    }
    """

    df = spark.createDataFrame(
        [(json_data,)],
        ["value"]
    )

    result = (
        transform_aqi(df)
        .collect()
    )

    assert result[0]["aqi"] == 2

    assert result[0]["pm25"] == 15.0