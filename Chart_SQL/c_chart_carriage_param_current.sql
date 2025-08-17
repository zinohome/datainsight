CREATE OR REPLACE VIEW c_chart_carriage_param_current AS
SELECT 
    dvc_train_no,
    dvc_carriage_no,
    param_name,
    param_value,
    report_time,
    data_source
FROM (
    SELECT 
        dvc_train_no,
        dvc_carriage_no,
        param_name,
        param_value,
        report_time,
        data_source,
        ROW_NUMBER() OVER (PARTITION BY dvc_train_no, param_name ORDER BY time DESC) AS rn
    FROM (
        -- 从视图获取数据
        (SELECT
            dvc_train_no,
            dvc_carriage_no,
            param_name,
            param_value,
            NULL AS report_time,
            'view' AS data_source,
            (SELECT MAX(msg_time) FROM (
                SELECT msg_calc_parse_time AS msg_time FROM dev_param_transposed WHERE dvc_train_no = c.dvc_train_no AND param_name = c.param_name
                UNION ALL
                SELECT msg_calc_dvc_time AS msg_time FROM pro_param_transposed WHERE dvc_train_no = c.dvc_train_no AND param_name = c.param_name
            ) AS sub) AS time
        FROM chart_carriage_param_current c) 

        UNION ALL

        -- 从表获取数据
        (SELECT
            dvc_train_no,
            dvc_carriage_no,
            param_name,
            param_value,
            report_time,
            'table' AS data_source,
            report_time AS time
        FROM n_chart_carriage_param_current)
    ) AS combined_data
) AS t
WHERE t.rn = 1;