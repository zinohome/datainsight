CREATE TABLE IF NOT EXISTS n_chart_view_param (
    report_time TIMESTAMP NOT NULL,
    time_minute TIMESTAMP NOT NULL,
    msg_calc_dvc_no TEXT NULL,
    msg_calc_train_no TEXT NOT NULL,
    dvc_train_no INTEGER NOT NULL,
    dvc_carriage_no INTEGER NOT NULL,
    param_name TEXT NOT NULL,
    measurement_count BIGINT NOT NULL,
    avg_value DOUBLE PRECISION,
    max_value DOUBLE PRECISION,
    min_value DOUBLE PRECISION,
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_view_param', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);