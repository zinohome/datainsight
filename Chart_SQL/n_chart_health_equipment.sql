CREATE TABLE IF NOT EXISTS n_chart_health_equipment (
    report_time TIMESTAMP NOT NULL,
    车号 INTEGER NOT NULL,
    车厢号 INTEGER NOT NULL,
    部件 TEXT NOT NULL,
    耗用率 NUMERIC(10, 2),
    额定寿命 NUMERIC(10, 2),
    已耗 DOUBLE PRECISION,
    PRIMARY KEY (report_time)
);

SELECT create_hypertable('n_chart_health_equipment', 'report_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);