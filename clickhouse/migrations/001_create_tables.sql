CREATE DATABASE IF NOT EXISTS sensor_logs_db;

USE sensor_logs_db;

-- CREATE TABLE IF NOT EXISTS sensor_logs (
--     timestamp DateTime64(3, 'Asia/Jakarta'),
--     sensor_id String,
--     channel String,
--     data_center String,
--     duration Float32,
--     measurement Float32,
--     product String,
--     status String,
--     type String,
--     unit String,
--     metadata String
-- ) ENGINE = MergeTree()
-- ORDER BY timestamp;

CREATE TABLE IF NOT EXISTS sensor_logs (
    timestamp DateTime64(6, 'Asia/Jakarta'),
    sensor_id String,
    channel String,
    data_center String,
    duration Float32,
    measurement Float32,
    product String,
    status String,
    type String,
    unit String,
    metadata String,
    latency Float32 MATERIALIZED dateDiff('microsecond', timestamp, now64())
) ENGINE = MergeTree()
ORDER BY timestamp;