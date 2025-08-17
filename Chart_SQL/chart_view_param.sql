CREATE OR REPLACE VIEW chart_view_param AS
-- 第一个查询：来自dev_param_transposed表
SELECT
    time_bucket('5 minute', msg_calc_parse_time) AT TIME ZONE 'Asia/Shanghai' AS time_minute,
    msg_calc_dvc_no,
    msg_calc_train_no,
    dvc_train_no,
    dvc_carriage_no,
    param_name,
    COUNT(*) as measurement_count,
    AVG(param_value) as avg_value,
    MAX(param_value) as max_value,
    MIN(param_value) as min_value
FROM dev_param_transposed
WHERE msg_calc_parse_time >= NOW() - INTERVAL '7 days'
    AND msg_calc_parse_time < NOW()
    AND param_name IS NOT NULL
    AND param_value IS NOT NULL
GROUP BY time_minute, msg_calc_dvc_no, msg_calc_train_no, dvc_train_no, dvc_carriage_no, param_name

UNION ALL

-- 第二个查询：来自pro_param_transposed表
SELECT
    time_bucket('5 minute', msg_calc_dvc_time) AT TIME ZONE 'Asia/Shanghai' AS time_minute,
    msg_calc_dvc_no,
    msg_calc_train_no,
    dvc_train_no,
    dvc_carriage_no,
    param_name,
    COUNT(*) as measurement_count,
    AVG(param_value) as avg_value,
    MAX(param_value) as max_value,
    MIN(param_value) as min_value
FROM pro_param_transposed
WHERE msg_calc_dvc_time >= NOW() - INTERVAL '7 days'
    AND msg_calc_dvc_time < NOW()
    AND param_name IS NOT NULL
    AND param_value IS NOT NULL
GROUP BY time_minute, msg_calc_dvc_no, msg_calc_train_no, dvc_train_no, dvc_carriage_no, param_name

-- 对合并后的结果进行排序
ORDER BY time_minute DESC, msg_calc_dvc_no, param_name;
