DROP VIEW IF EXISTS sensor_logs_db.avg_duration_mv_populate;
DROP TABLE IF EXISTS sensor_logs_db.avg_duration_mv;

DROP TABLE IF EXISTS sensor_logs_db.avg_duration_mv_populate;

CREATE TABLE sensor_logs_db.avg_duration_mv
(
    cnt AggregateFunction(count, UInt64),
    avg_duration AggregateFunction(avg, Float32)
)
ENGINE = AggregatingMergeTree()
ORDER BY tuple();

CREATE MATERIALIZED VIEW sensor_logs_db.avg_duration_mv_populate
TO sensor_logs_db.avg_duration_mv
AS
SELECT
    countState() AS cnt,
    avgState(duration) AS avg_duration
FROM sensor_logs_db.sensor_logs;

SELECT
    count() AS total_count,
    avg(duration) AS average_duration
FROM sensor_logs_db.sensor_logs;

SELECT
    countMerge(cnt) AS total_count,
    avgMerge(avg_duration) AS average_duration
FROM sensor_logs_db.avg_duration_mv;