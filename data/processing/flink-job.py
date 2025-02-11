import json

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcExecutionOptions, JdbcConnectionOptions
from pyflink.common.typeinfo import Types

from data.processing.config.utils import get_env

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

KAFKA_BROKER = get_env("KAFKA_BROKER")
KAFKA_TOPIC = get_env("KAFKA_TOPIC")
CLICKHOUSE_DB = get_env("CLICKHOUSE_DB")
CLICKHOUSE_TABLE = get_env("CLICKHOUSE_TABLE")

kafka_source = KafkaSource.builder() \
    .set_bootstrap_servers(KAFKA_BROKER) \
    .set_topics(KAFKA_TOPIC) \
    .set_group_id("flink_sensor_group") \
    .set_value_only_deserializer(Types.STRING()) \
    .build()

stream = env.from_source(kafka_source, watermark_strategy=None, source_name="Kafka Source")

def parse_json(value):
    try:
        data = json.loads(value)
        return (data["timestamp"], data["sensor_id"], data["measurement"], data["duration"],
                data["channel"], data["data_center"], data["product"], data["status"],
                data["type"], data["unit"], json.dumps(data["metadata"]))
    except Exception as e:
        return None

parsed_stream = stream.map(parse_json, output_type=Types.TUPLE([Types.STRING(), Types.STRING(), Types.FLOAT(),
                                                                Types.FLOAT(), Types.STRING(), Types.STRING(),
                                                                Types.STRING(), Types.STRING(), Types.STRING(),
                                                                Types.STRING(), Types.STRING()]))

sink = JdbcSink.sink(
    "INSERT INTO {CLICKHOUSE_TABLE} (timestamp, sensor_id, measurement, duration, channel, data_center, product, status, type, unit, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    type_info=Types.TUPLE([Types.STRING(), Types.STRING(), Types.FLOAT(), Types.FLOAT(), Types.STRING(), Types.STRING(),
                           Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING()]),
    jdbc_execution_options=JdbcExecutionOptions.builder()
        .with_batch_size(500)
        .with_batch_interval_ms(200)
        .with_max_retries(3)
        .build(),
    jdbc_connection_options=JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
        .with_url(CLICKHOUSE_DB)
        .with_driver_name("com.clickhouse.jdbc.ClickHouseDriver")
        .build()
)

parsed_stream.add_sink(sink)

env.execute("Flink Kafka to ClickHouse Job")
