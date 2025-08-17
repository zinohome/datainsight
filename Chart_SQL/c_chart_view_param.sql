CREATE OR REPLACE VIEW c_chart_view_param AS
-- 从n_chart_view_param表获取最新数据
SELECT
    time_minute,
    msg_calc_dvc_no,
    msg_calc_train_no,
    dvc_train_no,
    dvc_carriage_no,
    param_name,
    measurement_count,
    avg_value,
    max_value,
    min_value,
    'table' AS data_source
FROM (
    SELECT
        time_minute,
        msg_calc_dvc_no,
        msg_calc_train_no,
        dvc_train_no,
        dvc_carriage_no,
        param_name,
        measurement_count,
        avg_value,
        max_value,
        min_value,
        ROW_NUMBER() OVER (PARTITION BY dvc_train_no, dvc_carriage_no, param_name ORDER BY report_time DESC) AS rn
    FROM n_chart_view_param
) AS t
WHERE t.rn = 1

UNION ALL

-- 从chart_view_parem视图获取数据（注意：视图名称可能存在拼写错误，实际为chart_view_parem）
SELECT
    time_minute,
    msg_calc_dvc_no,
    msg_calc_train_no,
    dvc_train_no,
    dvc_carriage_no,
    param_name,
    measurement_count,
    avg_value,
    max_value,
    min_value,
    'view' AS data_source
FROM chart_view_param;