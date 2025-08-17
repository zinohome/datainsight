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




CREATE OR REPLACE VIEW chart_line_fault_param_type AS
SELECT
    combined.dvc_train_no,
    combined.fault_type AS "故障类型",
    combined.param_name AS "故障部件",
    sum(combined."故障数量") AS "故障数量"
FROM (
    SELECT
        dev_view_fault_timed_mat.dvc_train_no,
        dev_view_fault_timed_mat.fault_type,
        dev_view_fault_timed_mat.param_name,  -- 添加故障部件
        count(*) AS "故障数量"
    FROM dev_view_fault_timed_mat
    WHERE dev_view_fault_timed_mat.status = '持续'::text
    GROUP BY
        dev_view_fault_timed_mat.dvc_train_no,
        dev_view_fault_timed_mat.fault_type,
        dev_view_fault_timed_mat.param_name  -- 分组中加入故障部件

    UNION ALL

    SELECT
        pro_view_fault_timed_mat.dvc_train_no,
        pro_view_fault_timed_mat.fault_type,
        pro_view_fault_timed_mat.param_name,  -- 添加故障部件
        count(*) AS "故障数量"
    FROM pro_view_fault_timed_mat
    WHERE pro_view_fault_timed_mat.status = '持续'::text
    GROUP BY
        pro_view_fault_timed_mat.dvc_train_no,
        pro_view_fault_timed_mat.fault_type,
        pro_view_fault_timed_mat.param_name  -- 分组中加入故障部件
) combined
GROUP BY
    combined.dvc_train_no,
    combined.fault_type,
    combined.param_name  -- 外层分组也需要包含故障部件
ORDER BY
    combined.fault_type,
    combined.dvc_train_no,
    combined.param_name;  -- 按故障部件排序
