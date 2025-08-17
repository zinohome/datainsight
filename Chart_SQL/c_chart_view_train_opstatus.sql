CREATE OR REPLACE VIEW c_chart_view_train_opstatus AS
-- 处理n_chart_view_train_opstatus表数据
SELECT 
    dvc_train_no,
    latest_op_condition,
    latest_time,
    "立即维修",
    "加强跟踪",
    "计划维修",
    "正常运营",
    'table' AS data_source
FROM (
    SELECT 
        dvc_train_no,
        latest_op_condition,
        latest_time,
        "立即维修",
        "加强跟踪",
        "计划维修",
        "正常运营",
        ROW_NUMBER() OVER (PARTITION BY dvc_train_no ORDER BY report_time DESC) AS rn
    FROM n_chart_view_train_opstatus
) AS t
WHERE t.rn = 1

UNION ALL

-- 处理chart_view_train_opstatus视图数据
SELECT 
    dvc_train_no,
    latest_op_condition,
    latest_time,
    "立即维修",
    "加强跟踪",
    "计划维修",
    "正常运营",
    'view' AS data_source
FROM chart_view_train_opstatus;