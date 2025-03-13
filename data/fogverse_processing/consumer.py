import asyncio
from fogverse import KafkaConsumer

from config.constants import (
    KAFKA_BOOTSTRAP_SERVERS, 
    KAFKA_TOPIC,
    GROUP_ID
)

async def main():
    # Create the consumer with the appropriate configuration.
    # You can pass additional parameters like group_id and auto_offset_reset here.
    consumer = KafkaConsumer(
        topics=[KAFKA_TOPIC],
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID
    )

    await consumer.start()
    print(f"Listening for messages on topic: {KAFKA_TOPIC}")

    try:
        while True:
            # Wait for a new message asynchronously.
            msg = await consumer.receive()
            print("Received Message:", msg)
    except KeyboardInterrupt:
        print("\nStopping Kafka Consumer...")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(main())