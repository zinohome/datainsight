CREATE OR REPLACE VIEW chart_carriage_base AS
WITH latest_records AS (
    SELECT DISTINCT ON (dvc_train_no, param_name)
        dvc_train_no,
        dvc_carriage_no,
        param_name,
        param_value,
        msg_time
    FROM (
        -- 为dev表的查询添加括号包裹
        (SELECT
            dvc_train_no,
            dvc_carriage_no,
            param_name,
            param_value,
            msg_calc_parse_time AS msg_time
        FROM dev_param_transposed
        WHERE param_name IN ('空调运行模式U1', '目标温度', '新风温度-系统', '回风温度-系统')
        ORDER BY msg_calc_parse_time DESC
        LIMIT 5000)

        UNION ALL

        -- 为pro表的查询添加括号包裹
        (SELECT
            dvc_train_no,
            dvc_carriage_no,
            param_name,
            param_value,
            msg_calc_dvc_time AS msg_time
        FROM pro_param_transposed
        WHERE param_name IN ('空调运行模式U1', '目标温度', '新风温度-系统', '回风温度-系统')
        ORDER BY msg_calc_dvc_time DESC
        LIMIT 5000)
    ) AS combined_data
    ORDER BY dvc_train_no, param_name, msg_time DESC
)
SELECT
    dvc_train_no,
    dvc_carriage_no,
    MAX(param_value) FILTER (WHERE param_name = '空调运行模式U1') AS 运行模式,
    MAX(param_value) FILTER (WHERE param_name = '目标温度') AS 目标温度,
    MAX(param_value) FILTER (WHERE param_name = '新风温度-系统') AS 新风温度,
    MAX(param_value) FILTER (WHERE param_name = '回风温度-系统') AS 回风温度
FROM latest_records
GROUP BY dvc_train_no, dvc_carriage_no
ORDER BY dvc_train_no, dvc_carriage_no;