# Real-time Monitoring and Alerting in Industry Manufacturing

This project demonstrates a **real-time monitoring and alerting system for industrial manufacturing** using a scalable and modular architecture.

---

## Architecture Overview

![System Design](./images/System%20Design.png)

This system follows a **distributed streaming approach** where sensor data is collected, processed, stored, and visualized for real-time monitoring and alerting.

---

## Components Overview

### Edge Devices (Sensor Data Collection)
- **Devices:** Python-enabled microcontrollers or industrial IoT sensors.
- **Data Type:** Vibration, temperature, humidity, pressure, and electrical readings.
- **Logging:**
  - Uses a **custom Log SDK** to structure and log data.
  - **Implemented Approach:** Sensor data is logged both to local log files and forwarded to a Kafka topic.

### Apache Kafka (Message Broker & Data Streaming)
- Kafka acts as the central **message bus** for streaming raw sensor data.
- Ensures **fault tolerance** and **high availability**.

### Apache Flink (Stream Processing & ML Inference)
- **Extracts, Transforms, and Loads (ETL):** Processes real-time data from Kafka.
- **ML Inference:** Runs pre-trained ML models for anomaly detection.
  - **Recommendation:** Load pre-trained ML models directly within Flink jobs (Low Priority) for more efficient real-time inference.
- **Data Transformation:**
  - **Current Pipeline:** Direct pipeline from Kafka to ClickHouse.
  - **Future Enhancements:** Add advanced transformations (e.g., windowing, aggregating) to maximize batch insert efficiency and improve processing throughput (Medium Priority).

### ClickHouse (Analytical Database Engine)
- Optimized for high-speed **time-series data storage**.
- Stores both **raw** and **processed sensor data**.
- Allows fast querying for analytics and monitoring.
- **Recommendation:** Implement event-driven database housekeeping by triggering functions in ClickHouse (High Priority). For example, every 24 hours, merge daily data into a single summarized row in another table to improve memory usage and query performance.

### Grafana (Visualization & Alerting System)
- Provides real-time **dashboards** for visualizing sensor data.
- Enables threshold-based **alerting** for equipment failures.
- Connects directly to ClickHouse for querying data.

---

## Additional Data Processing & Storage Pipeline

Apart from real-time monitoring, the system includes a **batch data pipeline**:

1. **Monitor Log Files:** Utilizes the Elastic Stack.
2. **Convert Logs to CSV:** For structured analysis.
3. **Store Data in GCP Bucket:** For long-term retention.
   - **Recommendation (Low Priority):** Consider integrating backup storage solutions to further secure and archive data, although this is not based on a real-world example.
4. **Train ML Models in Jupyter Notebooks:** For future predictive maintenance.

---

## Implementation Details

- **Logging Mechanism:**
  The custom Log SDK is used to log sensor data both locally (log files) and to Kafka. This dual logging approach ensures that raw data is captured reliably and can be processed in real time.
  
- **Data Pipeline:**
  The implemented pipeline efficiently streams data from Kafka into ClickHouse, which is then visualized in Grafana. This ensures seamless data flow from sensor collection to end-user dashboards.

---

## Deployment & Scalability

### Dockerized Microservices Approach

Each component is **containerized** using Docker and orchestrated via **Docker Compose**. This setup ensures:

- **Scalability:** Additional sensors or processing nodes can be dynamically added.
- **Fault Tolerance:** Services are automatically restarted if a failure occurs.
- **Distributed Processing:** Both Flink and Kafka are capable of handling high-throughput sensor streams.

---

## Use Case: Industrial Machine Monitoring

### Scenario

- Industrial machines are equipped with **multiple sensors** monitoring operational conditions.
- Each sensor **sends real-time data** to Kafka.
- Flink **detects anomalies** such as sudden temperature spikes.
- Alerts are triggered in **Grafana** if any metric exceeds a safe threshold.
- Engineers receive alerts and can take **preventive action** before machine failure occurs.

---

## Future Enhancements and Recommendations

- **Backup Storage (Low Priority):**
  Explore integrating backup storage solutions to provide additional data redundancy and long-term archival.
  
- **Event-Driven Database Housekeeping (High Priority):**
  Implement trigger functions on ClickHouse to perform routine database housekeeping. For example, every 24 hours, merge daily records into a summarized row in a dedicated table to optimize memory usage.
  
- **Enhanced Flink Processing:**
  - **ML Model Integration (Low Priority):**
    Load pre-trained ML models directly within the Flink job to streamline real-time anomaly detection.
  - **Advanced Data Transformations (Medium Priority):**
    Incorporate additional transformation steps (e.g., windowing, aggregation) to leverage batch inserts more effectively and enhance the processing efficiency.

- **Automated Self-Healing Pipelines:**
  Future work could include developing automated mechanisms to detect and remediate sensor faults, further increasing system resilience.
  
- **More Advanced Predictive Maintenance Models:**
  Continue refining and training predictive maintenance models to improve early fault detection and operational efficiency.

---

## Conclusion

This architecture provides a **highly scalable, fault-tolerant, and real-time monitoring system** for industrial manufacturing. By leveraging Kafka, Flink, ClickHouse, and Grafana, industries can **prevent equipment failures, reduce downtime, and optimize performance**. The implemented solutions—such as the use of a custom Log SDK for dual logging and a streamlined pipeline from Kafka to ClickHouse to Grafana—combined with the proposed recommendations, lay a strong foundation for future enhancements in industrial monitoring systems.
