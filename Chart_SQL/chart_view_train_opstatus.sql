CREATE OR REPLACE VIEW chart_view_train_opstatus AS
SELECT
    dvc_train_no,
    MAX(latest_op_condition) AS latest_op_condition,  -- 取最新的运行状态
    MAX(latest_time) AS latest_time,                  -- 取最新的时间
    SUM("立即维修") AS "立即维修",
    SUM("加强跟踪") AS "加强跟踪",
    SUM("计划维修") AS "计划维修",
    SUM("正常运营") AS "正常运营"
FROM (
    -- 合并两个视图的数据
    SELECT * FROM dev_view_train_opstatus
    UNION ALL
    SELECT * FROM pro_view_train_opstatus
) AS combined_data
GROUP BY dvc_train_no
ORDER BY dvc_train_no;