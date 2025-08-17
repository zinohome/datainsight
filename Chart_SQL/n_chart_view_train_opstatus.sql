CREATE TABLE IF NOT EXISTS n_chart_view_train_opstatus (
    report_time TIMESTAMP NOT NULL,
    dvc_train_no INTEGER NOT NULL,
    latest_op_condition VARCHAR(50),
    latest_time TIMESTAMP,
    "立即维修" INTEGER NOT NULL,
    "加强跟踪" INTEGER NOT NULL,
    "计划维修" INTEGER NOT NULL,
    "正常运营" INTEGER NOT NULL,
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_view_train_opstatus', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);