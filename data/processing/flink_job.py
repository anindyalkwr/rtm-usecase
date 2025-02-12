import os
import logging

from pyflink.common import WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcExecutionOptions, JdbcConnectionOptions
from pyflink.datastream.formats.json import JsonRowDeserializationSchema

from config.utils import get_env
from models.sensor_data import SensorData

KAFKA_BOOTSTRAP_SERVERS = get_env("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = get_env("KAFKA_TOPIC")
FLINK_GROUP_ID = get_env("FLINK_GROUP_ID")

CLICKHOUSE_JDBC_URL = get_env("CLICKHOUSE_JDBC_URL")
CLICKHOUSE_TABLE = get_env("CLICKHOUSE_TABLE")

RUNTIME_ENV = get_env("RUNTIME_ENV", "local")

if __name__ == "__main__":
    """
    Submit a job to the Flink cluster using one of the commands below.

    Bash:
    -----
    docker exec jobmanager /opt/flink/bin/flink run \
    --python /tmp/src/flink_job.py \
    -pyFiles file:///tmp/src/src.zip \
    -d

    PowerShell:
    -----------
    docker exec jobmanager /opt/flink/bin/flink run `
    --python /tmp/src/flink_job.py `
    --pyFiles file:///tmp/src/src.zip `
    -d
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info(f"RUNTIME_ENV - {RUNTIME_ENV}, BOOTSTRAP_SERVERS - {KAFKA_BOOTSTRAP_SERVERS}")

    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)

    JAR_DIR = "/opt/flink/lib"
    jar_files = [
        "flink-sql-connector-kafka-1.17.1.jar",
        "flink-connector-jdbc-3.1.2-1.17.jar",
        "clickhouse-jdbc-0.4.6.jar"
    ]
    jar_paths = tuple(
        [f"file://{os.path.join(JAR_DIR, name)}" for name in jar_files]
    )

    logging.info(f"adding local jars - {', '.join(jar_files)}")
    env.add_jars(*jar_paths)

    kafka_source = (
        KafkaSource.builder()
        .set_bootstrap_servers(KAFKA_BOOTSTRAP_SERVERS) 
        .set_topics(KAFKA_TOPIC) 
        .set_group_id(FLINK_GROUP_ID)
        .set_starting_offsets(KafkaOffsetsInitializer.latest())
        .set_value_only_deserializer(
            JsonRowDeserializationSchema.builder()
            .type_info(SensorData.get_value_type_info())
            .build()
        )
        .build()
    )

    stream = env.from_source(
        kafka_source, watermark_strategy=WatermarkStrategy.no_watermarks(), source_name="Kafka Source"
    )

    stream.map(SensorData.from_row).print()

    sink = JdbcSink.sink(
        "INSERT INTO {} (timestamp, sensor_id, channel, data_center, duration, measurement, product, status, type, unit, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(CLICKHOUSE_TABLE),
        type_info=SensorData.get_value_type_info(),
        jdbc_execution_options=JdbcExecutionOptions.builder()
            .with_batch_size(100)
            .with_batch_interval_ms(200)
            .with_max_retries(3)
            .build(),
        jdbc_connection_options=JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url(CLICKHOUSE_JDBC_URL)
            .with_driver_name("com.clickhouse.jdbc.ClickHouseDriver")
            .build()
    )

    stream.add_sink(sink)

    env.execute("Flink Kafka to ClickHouse Job")