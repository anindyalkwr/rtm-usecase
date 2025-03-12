from confluent_kafka import Consumer

KAFKA_BOOTSTRAP_SERVERS = "192.168.59.103:30749,192.168.59.103:32272,192.168.59.103:31445"
KAFKA_TOPIC = "sensor-logs"

consumer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": "sensor_group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_config)
consumer.subscribe([KAFKA_TOPIC])

print(f"Listening for messages on topic: {KAFKA_TOPIC}")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        print(f"Received Message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("\n Stopping Kafka Consumer...")
finally:
    consumer.close()
