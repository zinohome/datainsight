CREATE TABLE IF NOT EXISTS d_chart_health_clean (
    clean_time TIMESTAMP NOT NULL,
    车号 INTEGER NOT NULL,
    车厢号 INTEGER NOT NULL,
    部件 TEXT NOT NULL,
    已耗 DOUBLE PRECISION,
    PRIMARY KEY (clean_time)
);
SELECT create_hypertable('d_chart_health_clean', 'clean_time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);
