from pyspark.sql import SparkSession

from pyspark.sql.functions import (
    col,
    from_json,
    current_timestamp
)

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType
)

weather_schema = StructType([

    StructField(
        "city",
        StringType()
    ),

    StructField(
        "temperature",
        DoubleType()
    ),

    StructField(
        "humidity",
        IntegerType()
    ),

    StructField(
        "pressure",
        IntegerType()
    ),

    StructField(
        "weather_condition",
        StringType()
    ),

    StructField(
        "wind_speed",
        DoubleType()
    ),

    StructField(
        "timestamp",
        StringType()
    )
])

def transform_weather(df):

    return (

        df.selectExpr(
            "CAST(value AS STRING)"
        )

        .select(

            from_json(
                col("value"),
                weather_schema
            ).alias("data")
        )

        .select(
            "data.*"
        )

        .withColumn(
            "ingestion_timestamp",
            current_timestamp()
        )
    )

def create_stream():

    spark = (

        SparkSession.builder

        .appName(
            "WeatherStream"
        )

        .getOrCreate()
    )

    kafka_df = (

        spark.readStream

        .format("kafka")

        .option(
            "kafka.bootstrap.servers",
            "localhost:9092"
        )

        .option(
            "subscribe",
            "weather_raw"
        )

        .load()
    )

    transformed_df = (
        transform_weather(
            kafka_df
        )
    )

    query = (

        transformed_df.writeStream

        .format("parquet")

        .option(
            "path",
            "s3a://smartcity360-datalake-dev/bronze/weather"
        )

        .option(
            "checkpointLocation",
            "/tmp/checkpoints/weather"
        )

        .outputMode(
            "append"
        )

        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    create_stream()