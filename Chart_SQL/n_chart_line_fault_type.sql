CREATE TABLE IF NOT EXISTS n_chart_line_fault_type (
    report_time TIMESTAMP NOT NULL,
    dvc_train_no INTEGER NOT NULL,
    "故障类型" TEXT NOT NULL,
    "故障数量" NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_line_fault_type', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);