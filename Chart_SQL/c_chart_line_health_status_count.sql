CREATE OR REPLACE VIEW c_chart_line_health_status_count AS
-- 从n_chart_line_health_status_count表获取最新数据
SELECT
    dvc_train_no,
    device_health_status,
    device_count,
    'table' AS data_source
FROM (
    SELECT
        dvc_train_no,
        device_health_status,
        device_count,
        ROW_NUMBER() OVER (PARTITION BY dvc_train_no, device_health_status ORDER BY report_time DESC) AS rn
    FROM n_chart_line_health_status_count
) AS t
WHERE t.rn = 1

UNION ALL

-- 从chart_line_health_status_count视图获取数据
SELECT
    dvc_train_no,
    device_health_status,
    device_count,
    'view' AS data_source
FROM chart_line_health_status_count;