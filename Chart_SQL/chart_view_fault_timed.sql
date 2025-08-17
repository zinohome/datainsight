CREATE OR REPLACE VIEW chart_view_fault_timed AS
    -- 第一部分：预警数据（来自预测视图，新增字段置空）
SELECT
    p.msg_calc_dvc_no,
    p.msg_calc_train_no,
    p.dvc_train_no,
    p.dvc_carriage_no,
    p.param_name,
    p.predict_start_time AS start_time,
    p.predict_end_time AS end_time,
    p.predict_status AS status,
    0 AS fault_level,  -- 预警无诊断等级，置空
    NULL::text AS repair_suggestion,  -- 预警无维修建议，置空
    '预警'::text AS fault_type
FROM dev_view_predict_timed_mat p

UNION ALL

-- 第二部分：故障诊断数据（来自错误诊断视图，包含新增字段）
SELECT
    d.msg_calc_dvc_no,
    d.msg_calc_train_no,
    d.dvc_train_no,
    d.dvc_carriage_no,
    d.param_name,
    d.error_start_time AS start_time,
    d.error_end_time AS end_time,
    d.error_status AS status,
    d.fault_level,  -- 故障诊断等级（来自关联表）
    d.repair_suggestion,  -- 维修建议（来自关联表）
    '故障'::text AS fault_type
FROM dev_view_error_diagnostic_mat d

UNION ALL

-- 第一部分：预警数据（来自预测视图，新增字段置空）
SELECT
    q.msg_calc_dvc_no,
    q.msg_calc_train_no,
    q.dvc_train_no,
    q.dvc_carriage_no,
    q.param_name,
    q.predict_start_time AS start_time,
    q.predict_end_time AS end_time,
    q.predict_status AS status,
    0 AS fault_level,  -- 预警无诊断等级，置空
    NULL::text AS repair_suggestion,  -- 预警无维修建议，置空
    '预警'::text AS fault_type
FROM pro_view_predict_timed_mat q

UNION ALL

-- 第二部分：故障诊断数据（来自错误诊断视图，包含新增字段）
SELECT
    e.msg_calc_dvc_no,
    e.msg_calc_train_no,
    e.dvc_train_no,
    e.dvc_carriage_no,
    e.param_name,
    e.error_start_time AS start_time,
    e.error_end_time AS end_time,
    e.error_status AS status,
    e.fault_level,  -- 故障诊断等级（来自关联表）
    e.repair_suggestion,  -- 维修建议（来自关联表）
    '故障'::text AS fault_type
FROM pro_view_error_diagnostic_mat e;



