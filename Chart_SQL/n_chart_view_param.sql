CREATE TABLE IF NOT EXISTS n_chart_view_param (
    report_time TIMESTAMP NOT NULL,
    time_minute TIMESTAMP NOT NULL,
    msg_calc_dvc_no VARCHAR(50) NOT NULL,
    msg_calc_train_no VARCHAR(50) NOT NULL,
    dvc_train_no INTEGER NOT NULL,
    dvc_carriage_no INTEGER NOT NULL,
    param_name VARCHAR(50) NOT NULL,
    measurement_count INTEGER NOT NULL,
    avg_value NUMERIC(10, 2),
    max_value NUMERIC(10, 2),
    min_value NUMERIC(10, 2),
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_view_param', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);