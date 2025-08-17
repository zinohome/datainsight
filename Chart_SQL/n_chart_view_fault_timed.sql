CREATE TABLE IF NOT EXISTS n_chart_view_fault_timed (
    report_time TIMESTAMP NOT NULL,
    msg_calc_dvc_no TEXT NULL,
    msg_calc_train_no TEXT NULL,
    dvc_train_no INTEGER NOT NULL,
    dvc_carriage_no INTEGER NOT NULL,
    param_name TEXT NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT,
    fault_level INTEGER,
    repair_suggestion TEXT,
    fault_type TEXT NOT NULL,
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_view_fault_timed', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);