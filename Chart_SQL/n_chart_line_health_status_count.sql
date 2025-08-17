CREATE TABLE IF NOT EXISTS n_chart_line_health_status_count (
    report_time TIMESTAMP NOT NULL,
    dvc_train_no INTEGER NOT NULL,
    device_health_status TEXT NOT NULL,
    device_count BIGINT NOT NULL,
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_line_health_status_count', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);