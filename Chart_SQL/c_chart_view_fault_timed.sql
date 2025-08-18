CREATE OR REPLACE VIEW c_chart_view_fault_timed AS
-- 合并n_chart_view_fault_timed表和chart_view_fault_timed视图数据，并排除已清理的故障记录
WITH combined_data AS (
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
    FROM chart_view_fault_timed
)
-- 排除与d_chart_fault_clean表中六个字段完全匹配的记录
SELECT cd.*
FROM combined_data cd
WHERE NOT EXISTS (
    SELECT 1
    FROM d_chart_fault_clean fc
    WHERE
        cd.dvc_train_no = fc.dvc_train_no
        AND cd.dvc_carriage_no = fc.dvc_carriage_no
        AND cd.param_name = fc.param_name
        AND cd.start_time = fc.start_time
        AND cd.fault_level = fc.fault_level
        AND cd.fault_type = fc.fault_type
);