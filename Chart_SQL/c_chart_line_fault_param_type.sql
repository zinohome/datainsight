CREATE OR REPLACE VIEW c_chart_line_fault_param_type AS
SELECT
    t.dvc_train_no,
    t."故障类型",
    t."故障部件",
    t."故障数量",
    t.report_time,
    'table' AS data_source
FROM (
    SELECT
        n_chart_line_fault_param_type.dvc_train_no,
        n_chart_line_fault_param_type."故障类型",
        n_chart_line_fault_param_type."故障部件",
        n_chart_line_fault_param_type."故障数量",
        n_chart_line_fault_param_type.report_time,
        ROW_NUMBER() OVER (
            PARTITION BY n_chart_line_fault_param_type.dvc_train_no, n_chart_line_fault_param_type."故障类型", n_chart_line_fault_param_type."故障部件"
            ORDER BY n_chart_line_fault_param_type.report_time DESC
        ) AS rn
    FROM n_chart_line_fault_param_type
) AS t
WHERE t.rn = 1

UNION ALL

SELECT
    chart_line_fault_param_type.dvc_train_no,
    chart_line_fault_param_type."故障类型",
    chart_line_fault_param_type."故障部件",
    chart_line_fault_param_type."故障数量",
    NULL AS report_time,
    'view' AS data_source
FROM chart_line_fault_param_type;