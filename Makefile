.PHONY: up-all down-all up-kafka up-clickhouse up-processing up-grafana up-input \
        down-kafka down-clickhouse down-processing down-grafana down-input

up-all:
	@echo "Deploying all services in order..."
	bash ./deploy.sh

down-all: down-kafka down-clickhouse down-processing down-grafana down-input
	@echo "All services have been brought down."

up-kafka:
	@echo "Starting Kafka..."
	(cd kafka && docker-compose up -d)

up-clickhouse:
	@echo "Starting ClickHouse..."
	(cd clickhouse && docker-compose up -d)

up-processing:
	@echo "Starting Data Processing..."
	(cd data/processing && docker-compose up -d)

up-grafana:
	@echo "Starting Grafana..."
	(cd grafana && docker-compose up -d)

up-input:
	@echo "Starting Data Input..."
	(cd data/input && docker-compose up -d)

### Individual DOWN targets ###

down-kafka:
	@echo "Stopping Kafka..."
	(cd kafka && docker-compose down)

down-clickhouse:
	@echo "Stopping ClickHouse..."
	(cd clickhouse && docker-compose down)

down-processing:
	@echo "Stopping Data Processing..."
	(cd data/processing && docker-compose down)

down-grafana:
	@echo "Stopping Grafana..."
	(cd grafana && docker-compose down)

down-input:
	@echo "Stopping Data Input..."
	(cd data/input && docker-compose down)
