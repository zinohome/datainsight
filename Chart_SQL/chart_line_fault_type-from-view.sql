CREATE OR REPLACE VIEW chart_line_fault_type AS
SELECT
    dvc_train_no,
    fault_type AS 故障类型,
    SUM(故障数量) AS 故障数量
FROM 
(SELECT
        dvc_train_no,
        fault_type,
        COUNT(*) AS 故障数量
    FROM c_chart_view_fault_timed
    WHERE status = '持续'
    GROUP BY dvc_train_no, fault_type
	) AS combined 
GROUP BY dvc_train_no, fault_type
ORDER BY 故障类型, dvc_train_no;