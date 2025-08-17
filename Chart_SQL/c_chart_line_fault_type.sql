CREATE OR REPLACE VIEW c_chart_line_fault_type AS
-- 从n_chart_line_fault_type表获取最新数据
SELECT
    dvc_train_no,
    "故障类型",
    "故障数量",
    'table' AS data_source
FROM (
    SELECT
        dvc_train_no,
        "故障类型",
        "故障数量",
        ROW_NUMBER() OVER (PARTITION BY dvc_train_no, "故障类型" ORDER BY report_time DESC) AS rn
    FROM n_chart_line_fault_type
) AS t
WHERE t.rn = 1

UNION ALL

-- 从chart_line_fault_type视图获取数据
SELECT
    dvc_train_no,
    "故障类型",
    "故障数量",
    'view' AS data_source
FROM chart_line_fault_type;