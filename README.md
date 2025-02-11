# Real-time Monitoring and Alerting in Industry Manufacturing

This project demonstrates a **real-time monitoring and alerting system for industrial manufacturing** using a scalable and modular architecture.

---

## **Architecture Overview**
![System Design](./images/System%20Design.png)

This system follows a **distributed streaming approach** where sensor data is collected, processed, stored, and visualized for real-time monitoring and alerting.

---

## **Components Overview**
### **Edge Devices (Sensor Data Collection)**
- **Devices:** Python-enabled microcontrollers or industrial IoT sensors.
- **Data Type:** Vibration, temperature, humidity, pressure, and electrical readings.
- **Logging:** Uses a **custom SDK** to structure logs and sending them to Kafka.

### **Apache Kafka (Message Broker & Data Streaming)**
- Kafka acts as the central **message bus** for streaming raw sensor data.
- Ensures **fault tolerance** and **high availability**.

### **Apache Flink (Stream Processing & ML Inference)**
- **Extracts, Transforms, and Loads (ETL)** real-time data from Kafka.
- Runs **pre-trained ML models** for anomaly detection.
- Stores **processed data and predictions** in ClickHouse.

### **ClickHouse (Analytical Database Engine)**
- Optimized for high-speed **time-series data storage**.
- Stores both **raw** and **processed sensor data**.
- Allows fast querying for analytics and monitoring.

### **Grafana (Visualization & Alerting System)**
- Provides real-time **dashboards** for visualizing sensor data.
- Enables threshold-based **alerting** for equipment failures.
- Connects directly to ClickHouse for querying data.

---

## **Additional Data Processing & Storage Pipeline**
Apart from real-time monitoring, this system also includes a **batch data pipeline**:
1. **Monitor Log Files** using **Elastic Stack**.
2. **Convert Logs to CSV** for structured analysis.
3. **Store Data in GCP Bucket** for long-term retention.
4. **Train ML Models in Jupyter Notebooks** for future predictive maintenance.

---

## **Deployment & Scalability**
### **Dockerized Microservices Approach**
Each component is **containerized** using Docker and orchestrated via **Docker Compose**. This setup ensures:
- **Scalability**: More sensors or processing nodes can be added dynamically.
- **Fault Tolerance**: If a service fails, it can restart automatically.
- **Distributed Processing**: Flink and Kafka can handle high-throughput sensor streams.

---

## **Use Case: Industrial Machine Monitoring**
### **Scenario**
- Industrial machines have **multiple sensors** monitoring operational conditions.
- Each sensor **sends real-time data** to Kafka.
- Flink **detects anomalies** like sudden temperature spikes.
- Alerts are triggered in **Grafana** if any metric exceeds a safe threshold.
- Engineers receive alerts and take **preventive action** before machine failure.

---

## **Future Enhancements**
- Integration with **edge AI models** for local anomaly detection.
- Automated **self-healing pipelines** for sensor faults.
- More advanced **predictive maintenance models**.

---

## **Conclusion**
This architecture provides a **highly scalable, fault-tolerant, and real-time monitoring system** for industrial manufacturing. By leveraging Kafka, Flink, ClickHouse, and Grafana, industries can **prevent equipment failures, reduce downtime, and optimize performance**.
