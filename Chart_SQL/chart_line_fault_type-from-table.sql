CREATE OR REPLACE VIEW chart_line_fault_type AS
SELECT
    dvc_train_no,
    fault_type AS 故障类型,
    SUM(故障数量) AS 故障数量
FROM (
    -- 从第一个视图获取数据
    SELECT
        dvc_train_no,
        fault_type,
        COUNT(*) AS 故障数量
    FROM dev_view_fault_timed_mat
    WHERE status = '持续'
    GROUP BY dvc_train_no, fault_type

    UNION ALL

    -- 从第二个视图获取数据
    SELECT
        dvc_train_no,
        fault_type ,
        COUNT(*) AS 故障数量
    FROM pro_view_fault_timed_mat
    WHERE status = '持续'
    GROUP BY dvc_train_no, fault_type
) AS combined
GROUP BY dvc_train_no, fault_type
ORDER BY 故障类型, dvc_train_no;