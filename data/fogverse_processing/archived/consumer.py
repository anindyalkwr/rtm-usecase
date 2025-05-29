import asyncio
import json
from datetime import datetime
from urllib.parse import urlparse
from fogverse import KafkaConsumer
from clickhouse_driver import Client
from config.constants import (
    KAFKA_BOOTSTRAP_SERVERS, 
    KAFKA_TOPIC,
    GROUP_ID,
    CLICKHOUSE_HOST,
    CLICKHOUSE_PORT,
    CLICKHOUSE_USERNAME,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_DATABASE,
    CLICKHOUSE_TABLE
)

class ClickHouseInserter:
    def __init__(self):
        self.client = Client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            user=CLICKHOUSE_USERNAME,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE,
            settings={'use_numpy': False}
        )
    
    async def insert_data(self, data):
        try:
            query = f"""
            INSERT INTO {CLICKHOUSE_TABLE} (
                timestamp, sensor_id, channel, data_center, duration,
                measurement, product, status, type, unit, metadata
            ) VALUES (%(timestamp)s, %(sensor_id)s, %(channel)s, %(data_center)s, 
                     %(duration)s, %(measurement)s, %(product)s, %(status)s, 
                     %(type)s, %(unit)s, %(metadata)s)
            """
            self.client.execute(query, data)
            print(f"Inserted data from sensor {data['sensor_id']} at {data['timestamp']}")
        except Exception as e:
            print(f"Error inserting data: {e}")

async def main():
    consumer = KafkaConsumer(
        topics=[KAFKA_TOPIC],
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
    )
    
    inserter = ClickHouseInserter()

    await consumer.start()
    print(f"Listening for messages on topic: {KAFKA_TOPIC}")

    try:
        while True:
            msg = await consumer.receive()
            print("Received raw message:", msg)
            
            try:
                msg_data = json.loads(msg)
            except json.JSONDecodeError as e:
                print(f"Failed to parse message: {e}")
                continue
                
            data = {
                'timestamp': msg_data['timestamp'],
                'sensor_id': str(msg_data['sensor_id']),
                'channel': str(msg_data['channel']),
                'data_center': str(msg_data['data_center']),
                'duration': float(msg_data['duration']),
                'measurement': float(msg_data['measurement']),
                'product': str(msg_data['product']),
                'status': str(msg_data['status']),
                'type': str(msg_data['type']),
                'unit': str(msg_data['unit']),
                'metadata': json.dumps(msg_data['metadata'])
            }
            
            # await asyncio.sleep(0.2)
            await inserter.insert_data(data)
            
    except KeyboardInterrupt:
        print("\nStopping Kafka Consumer...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        await consumer.stop()
        inserter.client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())