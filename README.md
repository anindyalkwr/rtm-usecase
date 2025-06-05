# Real-time Monitoring and Alerting in Industry Manufacturing

This project demonstrates a **real-time monitoring and alerting system for industrial manufacturing**, built with a **modular and scalable architecture** designed for continuous processing and high availability.


## Architecture Overview

### System Design

The architecture is divided into several layers, starting from sensor data collection to final visualization and alerting.

![System Design](./images/Overview%201.png)

### Real-Time Analytics Framework

![System Design](./images/Overview%202%20(b).png)

The data flows from:

* **Data Sources** (IoT sensors capturing metrics such as temperature, vibration, and pressure), into
* **Real-time Analytics**, where a custom **SDK Logger** logs sensor data locally for archival and publishes it to a **Kafka Cluster**.
* Kafka messages are consumed by a **KEDA-driven Consumer**, which can interact with external side services such as REST APIs, caches, or ML models for enrichment.
* Processed outputs are then stored in **ClickHouse**, an OLAP analytical time-series database.
* Finally, **Grafana** queries ClickHouse for real-time dashboards, while **Prometheus** scrapes system metrics for infrastructure-level insights.

## How to Reproduce the Experiment

The system includes infrastructure services running in Docker containers and a data pipeline running across Kubernetes-managed producers and consumers.

### Step 1: Set Up Infrastructure

Ensure Docker is installed. Then use the following commands to start each infrastructure component:

```bash
make kafka-up       # Starts Kafka (KRaft) broker and Exporters
make clickhouse-up  # Starts ClickHouse service
make prometheus-up  # Starts Prometheus
make grafana-up     # Starts Grafana dashboard
```

> Note: Avoid using legacy Flink-related scripts such as `deploy.sh` and legacy `Makefile` targets.

### Step 2: Deploy Producer and Consumer

Make sure you have access to a Kubernetes cluster and the **KEDA operator** installed. For KEDA installation via Helm, please refer to the Fogverse GitHub repository.

#### Deploying the Producer

Navigate to the `data/input` directory. The producer deployment includes configuration and deployment manifests:

```bash
kubectl apply -f k8s/sensor-producer-configmap.yaml
kubectl apply -f k8s/sensor-producer-deployment.yaml
```

This deploys the sensor data producer used to simulate incoming industrial metrics.

> To use the same setup used in the thesis experiment, run the scripts provided in the `data/experiment` folder.

#### Running the Consumer

The consumer is located in the `data/fogverse_processing` directory. After KEDA is set up, simply run:

```bash
python consumer.py
```

The consumer will connect to the Kafka topic and begin processing messages. KEDA will automatically manage the number of consumer replicas based on Kafka lag.

### Step 3: Run the Experiment

To simulate workload and drive the pipeline:

```bash
cd data/experiment
```

Run the experiment script:

* On Windows:

```cmd
run_experiment.bat
```

* On macOS/Linux: Modify or adapt the script as needed for your operating system.


## Use Case: Industrial Machine Monitoring

### Scenario

- Industrial machines are equipped with **multiple sensors** monitoring operational conditions.
- Each sensor **sends real-time data** to Kafka.
- Consumers **detects anomalies** such as sudden temperature spikes.
- Alerts are triggered in **Grafana** if any metric exceeds a safe threshold.
- Engineers receive alerts and can take **preventive action** before machine failure occurs.


## Future Enhancements and Recommendations

- **Backup Storage (Low Priority):**
  Explore integrating backup storage solutions to provide additional data redundancy and long-term archival.

- **Automated Self-Healing Pipelines (High Priority):**
  Future work could include developing automated mechanisms to detect and remediate sensor faults, further increasing system resilience.
  
- **Predictive Scaling (High Priority):**
  Implementing intelligent auto-scaling mechanisms for consumers based on predictive analytics.


## Conclusion

This architecture provides a **highly scalable, fault-tolerant, and real-time monitoring system** for industrial manufacturing. By leveraging Kafka, KEDA Consumer, ClickHouse, and Grafana, industries can **prevent equipment failures, reduce downtime, and optimize performance**. The implemented solutions—such as the use of a custom Log SDK for dual logging and a streamlined pipeline from Kafka to ClickHouse to Grafana—combined with the proposed recommendations, lay a strong foundation for future enhancements in industrial monitoring systems.

