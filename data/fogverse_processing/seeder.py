import json
import random
from datetime import datetime, timedelta
from clickhouse_driver import Client

# Connection settings from environment
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 9000
CLICKHOUSE_USERNAME = "admin"
CLICKHOUSE_PASSWORD = "admin_password"
CLICKHOUSE_DATABASE = "sensor_logs_db"
CLICKHOUSE_TABLE = "sensor_logs"

# Connect to ClickHouse
client = Client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT,
    user=CLICKHOUSE_USERNAME,
    password=CLICKHOUSE_PASSWORD,
    database=CLICKHOUSE_DATABASE
)

def generate_log():
    ts = datetime.now() - timedelta(seconds=random.randint(0, 100000))
    return {
        "timestamp": ts,
        "sensor_id": "sensor-local",
        "channel": "Sensor",
        "data_center": "Factory 1",
        "duration": round(random.uniform(1.0, 5.0), 2),
        "measurement": round(random.uniform(5.0, 15.0), 2),
        "product": "Machine Monitoring",
        "status": "Normal",
        "type": "Electrical Sensor",
        "unit": "A",
        "metadata": json.dumps({
            "machine_status": "Start",
            "uptime": round(random.random(), 6)
        })
    }

def insert_data(batch_size=1000000):
    batch = []
    for _ in range(batch_size):
        log = generate_log()
        batch.append([
            log['timestamp'], log['sensor_id'], log['channel'], log['data_center'],
            log['duration'], log['measurement'], log['product'], log['status'],
            log['type'], log['unit'], log['metadata']
        ])

    print(f"Inserting {batch_size} rows into {CLICKHOUSE_TABLE}...")
    client.execute(
        f'''
        INSERT INTO {CLICKHOUSE_TABLE}
        (timestamp, sensor_id, channel, data_center, duration, measurement, product, status, type, unit, metadata)
        VALUES
        ''',
        batch
    )
    print("Insert completed.")

if __name__ == "__main__":
    insert_data(4000000)  # Adjust to 50000, 150000 as needed
