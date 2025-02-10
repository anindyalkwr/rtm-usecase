CREATE TABLE IF NOT EXISTS sensor_logs (
    timestamp DateTime,
    sensor_id String,
    measurement Float32,
    duration Float32,
    channel String,
    data_center String,
    product String,
    status String,
    type String,
    unit String,
    metadata String
) ENGINE = MergeTree()
ORDER BY timestamp;
