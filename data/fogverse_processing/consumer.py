from fogverse.auto_scaling import KafkaConsumerConfig, KedaScalerConfig, KafkaKedaConsumer
# Example usage:

# Define Kafka consumer settings
consumer_config = KafkaConsumerConfig(
    topics=["sensor-logs"],
    bootstrap_servers="host.docker.internal:9094",
    group_id="scaling_sensor_group"
)

# Define KEDA scaling settings
scaler_config = KedaScalerConfig(
    min_replicas=0,
    max_replicas=10,
    lag_threshold=10
)

# Define additional environment variables if needed
additional_env_vars = {
    "CUSTOM_VAR": "custom_value",
    "ANOTHER_VAR": "another_value",
    "CLICKHOUSE_HOST": "host.docker.internal",
    "CLICKHOUSE_PORT": "9000", 
    "CLICKHOUSE_USERNAME": "admin",
    "CLICKHOUSE_PASSWORD": "admin_password",
    "CLICKHOUSE_DATABASE": "sensor_logs_db",
    "CLICKHOUSE_TABLE": "sensor_logs"
}

# Deploy Kafka consumer with KEDA, including custom env variables
consumer = KafkaKedaConsumer(
    name="fogverse-processing",
    image="anindyalkwr/fogverse_processing:latest",
    consumer_config=consumer_config,
    scaler_config=scaler_config,
    namespace="default",
    env_vars=additional_env_vars
)

consumer.deploy()
