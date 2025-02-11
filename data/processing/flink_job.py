import os
import json
import logging

from pyflink.common import WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
# from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcExecutionOptions, JdbcConnectionOptions
# from pyflink.common.typeinfo import Types

# from data.processing.config.utils import get_env

# KAFKA_BOOTSTRAP_SERVERS = get_env("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
# KAFKA_TOPIC = get_env("KAFKA_TOPIC", "sensor_logs")
# CLICKHOUSE_DB = get_env("CLICKHOUSE_DB")
# CLICKHOUSE_TABLE = get_env("CLICKHOUSE_TABLE")

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "sensor_logs"

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info(f"")

    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
    # env.set_parallelism(1)

    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    jar_files = ["flink-sql-connector-kafka-1.17.1.jar"]
    jar_paths = tuple(
        [f"file://{os.path.join(CURRENT_DIR, 'jars', name)}" for name in jar_files]
    )
    logging.info(f"{CURRENT_DIR}")
    logging.info(f"adding local jars - {', '.join(jar_files)}")
    env.add_jars("file:///opt/flink/lib/flink-sql-connector-kafka-1.17.1.jar")

    kafka_source = (
        KafkaSource.builder()
        .set_bootstrap_servers("kafka:9092") 
        .set_topics("sensor_logs") 
        .set_group_id("flink_sensor_group")
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        .set_value_only_deserializer(
            SimpleStringSchema()
        )
        .build()
    )

    stream = env.from_source(
        kafka_source, watermark_strategy=WatermarkStrategy.no_watermarks(), source_name="Kafka Source"
    )

    stream.print()

    env.execute("Flink Kafka to ClickHouse Job")

    # def parse_json(value):
    #     try:
    #         data = json.loads(value)
    #         return (
    #             data["timestamp"],
    #             data["sensor_id"],
    #             data["channel"],
    #             data["data_center"],
    #             data["duration"],
    #             data["measurement"],
    #             data["product"],
    #             data["status"],
    #             data["type"],
    #             data["unit"],
    #             json.dumps(data["metadata"])
    #         )
    #     except Exception as e:
    #         return None

    # parsed_stream = stream.map(
    #     parse_json, 
    #     output_type=Types.TUPLE([
    #         Types.STRING(),  
    #         Types.STRING(),  
    #         Types.STRING(),
    #         Types.STRING(),  
    #         Types.FLOAT(),   
    #         Types.FLOAT(),   
    #         Types.STRING(),  
    #         Types.STRING(),  
    #         Types.STRING(), 
    #         Types.STRING(), 
    #         Types.STRING()   
    #     ])
    # )

    # sink = JdbcSink.sink(
    #     "INSERT INTO {CLICKHOUSE_TABLE} (timestamp, sensor_id, channel, data_center, duration, measurement, product, status, type, unit, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #     type_info=Types.TUPLE([
    #         Types.STRING(),  
    #         Types.STRING(),  
    #         Types.STRING(),
    #         Types.STRING(),  
    #         Types.FLOAT(),   
    #         Types.FLOAT(),   
    #         Types.STRING(),  
    #         Types.STRING(),  
    #         Types.STRING(), 
    #         Types.STRING(), 
    #         Types.STRING()
    #     ]),
    #     jdbc_execution_options=JdbcExecutionOptions.builder()
    #         .with_batch_size(500)
    #         .with_batch_interval_ms(200)
    #         .with_max_retries(3)
    #         .build(),
    #     jdbc_connection_options=JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
    #         .with_url(CLICKHOUSE_DB)
    #         .with_driver_name("com.clickhouse.jdbc.ClickHouseDriver")
    # #         .build()
    # # )

    # parsed_stream.add_sink(sink)