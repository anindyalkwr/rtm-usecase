#!/bin/bash
set -e

wait_for_port() {
  local host=$1
  local port=$2
  echo "Waiting for ${host}:${port} to be ready..."
  while ! (echo > /dev/tcp/${host}/${port}) 2>/dev/null; do
    echo "  ${host}:${port} not ready, waiting..."
    sleep 1
  done
  echo "${host}:${port} is ready!"
}


### 1. Start Kafka ###
echo "Starting Kafka..."
(cd kafka && docker-compose up -d)

wait_for_port "localhost" "9092"

echo "Creating Kafka topic sensor_logs..."
MSYS_NO_PATHCONV=1 docker exec kafka /usr/bin/kafka-topics --create \
  --topic sensor_logs \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 || echo "Topic sensor_logs might already exist or an error occurred."


### 2. Start ClickHouse ###
echo "Starting ClickHouse..."
(cd clickhouse && docker-compose up -d)

echo "Waiting for ClickHouse to be ready..."
until docker exec clickhouse clickhouse-client --query "SELECT 1" >/dev/null 2>&1; do
  echo "ClickHouse not ready, waiting..."
  sleep 2
done
echo "ClickHouse is ready!"

echo "Executing migration files..."
MIGRATION_DIR="//migrations"

for file in $(docker exec clickhouse sh -c "ls $MIGRATION_DIR/*.sql"); do
  if [ -n "$file" ]; then
    echo "Running migration: $file"
    docker exec clickhouse sh -c "clickhouse-client --query \"$(docker exec clickhouse cat $file)\""
    if [ $? -ne 0 ]; then
      echo "Error applying migration $file"
      exit 1
    fi
  fi
done
echo "All migrations applied successfully."


### 3. Start Data Processing ###
echo "Starting Data Processing..."
(cd data/processing && docker-compose up -d)

### 3.5 Submit Flink Job ###
echo "Waiting for Flink JobManager to be ready on port 8081..."
wait_for_port "localhost" "8081"
echo "Flink JobManager is ready. Submitting job..."

# Submit the job to the Flink cluster (using the Bash command)
MSYS_NO_PATHCONV=1 docker exec jobmanager /opt/flink/bin/flink run \
  --python /tmp/src/flink_job.py \
  -pyFiles file:///tmp/src/src.zip \
  -d

# For PowerShell, you might use (uncomment if needed):
# MSYS_NO_PATHCONV=1 docker exec jobmanager /opt/flink/bin/flink run `
#   --python /tmp/src/flink_job.py `
#   --pyFiles file:///tmp/src/src.zip `
#   -d


### 4. Start Grafana ###
echo "Starting Grafana..."
(cd grafana && docker-compose up -d)


### 5. Start Data Input ###
echo "Starting Data Input..."
(cd data/input && docker-compose up -d)

echo "All services have been started."
