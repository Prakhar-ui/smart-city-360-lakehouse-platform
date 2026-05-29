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
    DoubleType
)

traffic_schema = StructType([

    StructField(
        "city",
        StringType()
    ),

    StructField(
        "current_speed",
        DoubleType()
    ),

    StructField(
        "free_flow_speed",
        DoubleType()
    ),

    StructField(
        "congestion_percentage",
        DoubleType()
    ),

    StructField(
        "timestamp",
        StringType()
    )
])

def transform_traffic(df):

    return (

        df.selectExpr(
            "CAST(value AS STRING)"
        )

        .select(
            from_json(
                col("value"),
                traffic_schema
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
            "TrafficStream"
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
            "traffic_raw"
        )

        .load()
    )

    transformed_df = (
        transform_traffic(
            kafka_df
        )
    )

    query = (

        transformed_df.writeStream

        .format("parquet")

        .option(
            "path",
            "s3a://smartcity360-datalake-dev/bronze/traffic"
        )

        .option(
            "checkpointLocation",
            "/tmp/checkpoints/traffic"
        )

        .outputMode(
            "append"
        )

        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    create_stream()