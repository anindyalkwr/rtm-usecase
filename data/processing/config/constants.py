from config.utils import get_env

KAFKA_BOOTSTRAP_SERVERS = get_env("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = get_env("KAFKA_TOPIC")
FLINK_GROUP_ID = get_env("FLINK_GROUP_ID")

CLICKHOUSE_URL = get_env("CLICKHOUSE_URL")
CLICKHOUSE_USERNAME = get_env("CLICKHOUSE_USERNAME")
CLICKHOUSE_PASSWORD = get_env("CLICKHOUSE_PASSWORD")
CLICKHOUSE_TABLE = get_env("CLICKHOUSE_TABLE")

RUNTIME_ENV = get_env("RUNTIME_ENV", "local")
LOG_LEVEL = get_env("LOG_LEVEL", "INFO").upper()