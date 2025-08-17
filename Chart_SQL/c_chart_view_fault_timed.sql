CREATE OR REPLACE VIEW c_chart_view_fault_timed AS
-- 从n_chart_view_fault_timed表获取最新数据
SELECT
    msg_calc_dvc_no,
    msg_calc_train_no,
    dvc_train_no,
    dvc_carriage_no,
    param_name,
    start_time,
    end_time,
    status,
    fault_level,
    repair_suggestion,
    fault_type,
    'table' AS data_source
FROM (
    SELECT
        msg_calc_dvc_no,
        msg_calc_train_no,
        dvc_train_no,
        dvc_carriage_no,
        param_name,
        start_time,
        end_time,
        status,
        fault_level,
        repair_suggestion,
        fault_type,
        ROW_NUMBER() OVER (PARTITION BY dvc_train_no, dvc_carriage_no, param_name, start_time ORDER BY report_time DESC) AS rn
    FROM n_chart_view_fault_timed
) AS t
WHERE t.rn = 1

UNION ALL

-- 从chart_view_fault_timed视图获取数据
SELECT
    msg_calc_dvc_no,
    msg_calc_train_no,
    dvc_train_no,
    dvc_carriage_no,
    param_name,
    start_time,
    end_time,
    status,
    fault_level,
    repair_suggestion,
    fault_type,
    'view' AS data_source
FROM chart_view_fault_timed;