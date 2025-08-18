CREATE TABLE IF NOT EXISTS d_chart_fault_clean (
    clean_time TIMESTAMP NOT NULL,
    dvc_train_no INTEGER NOT NULL,
    dvc_carriage_no INTEGER NOT NULL,
    param_name TEXT NOT NULL,
    start_time TIMESTAMP,
    fault_level INTEGER,
    fault_type TEXT NOT NULL,
    PRIMARY KEY (clean_time)
);

SELECT create_hypertable('d_chart_fault_clean', 'clean_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);