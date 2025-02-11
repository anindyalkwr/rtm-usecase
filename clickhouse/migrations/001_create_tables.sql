CREATE TABLE IF NOT EXISTS sensor_logs (
    timestamp DateTime64(3, 'Asia/Jakarta'),
    sensor_id String,
    channel String,
    data_center String,
    duration Float32,
    measurement Float32,
    product String,
    status String,
    type String,
    unit String,
    metadata String
) ENGINE = MergeTree()
ORDER BY timestamp;
