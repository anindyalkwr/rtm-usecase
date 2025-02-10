from confluent_kafka import Consumer

KAFKA_BROKERS = "localhost:9094"
KAFKA_TOPIC = "sensor_logs"

consumer_config = {
    "bootstrap.servers": KAFKA_BROKERS,
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
