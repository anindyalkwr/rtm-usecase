from config.utils import get_env

KAFKA_BOOTSTRAP_SERVERS = get_env("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = get_env("KAFKA_TOPIC", "sensor-logs")
GROUP_ID = get_env("GROUP_ID", "scaling_sensor_group")