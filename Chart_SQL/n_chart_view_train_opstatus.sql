CREATE TABLE IF NOT EXISTS n_chart_view_train_opstatus (
    report_time TIMESTAMP NOT NULL,
    dvc_train_no INTEGER NOT NULL,
    latest_op_condition INTEGER,
    latest_time TIMESTAMP,
    "立即维修" NUMERIC(10,2) NOT NULL,
    "加强跟踪" NUMERIC(10,2) NOT NULL,
    "计划维修" NUMERIC(10,2) NOT NULL,
    "正常运营" BIGINT NOT NULL,
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_view_train_opstatus', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);