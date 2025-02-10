FROM flink:1.16-scala_2.12

# Install dependencies
RUN pip install apache-flink clickhouse-driver

# Copy job script
COPY flink-job.py /flink-job.py

# Run Flink job
CMD ["python", "/flink-job.py"]
