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

aqi_schema = StructType([

    StructField(
        "city",
        StringType()
    ),

    StructField(
        "aqi",
        IntegerType()
    ),

    StructField(
        "pm25",
        DoubleType()
    ),

    StructField(
        "pm10",
        DoubleType()
    ),

    StructField(
        "timestamp",
        StringType()
    )
])

def transform_aqi(df):

    return (

        df.selectExpr(
            "CAST(value AS STRING)"
        )

        .select(
            from_json(
                col("value"),
                aqi_schema
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
            "AqiStream"
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
            "aqi_raw"
        )

        .load()
    )

    transformed_df = (
        transform_aqi(
            kafka_df
        )
    )

    query = (

        transformed_df.writeStream

        .format("parquet")

        .option(
            "path",
            "s3a://smartcity360-datalake-dev/bronze/aqi"
        )

        .option(
            "checkpointLocation",
            "/tmp/checkpoints/aqi"
        )

        .outputMode(
            "append"
        )

        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    create_stream()