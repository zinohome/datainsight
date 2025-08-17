CREATE TABLE IF NOT EXISTS n_chart_carriage_base (
    report_time TIMESTAMP NOT NULL,
    dvc_train_no INTEGER NOT NULL,
    dvc_carriage_no INTEGER NOT NULL,
    运行模式 DOUBLE PRECISION,
    目标温度 DOUBLE PRECISION,
    新风温度 DOUBLE PRECISION,
    回风温度 DOUBLE PRECISION,
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_carriage_base', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);