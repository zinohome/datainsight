CREATE OR REPLACE VIEW chart_carriage_param AS
WITH latest_records AS (
    -- 合并dev和pro表的数据，各取最新5000条
    (SELECT
        dvc_train_no,
        dvc_carriage_no,
        param_name,
        param_value,
        msg_calc_parse_time AS msg_time  -- dev表的时间字段
    FROM dev_param_transposed
    WHERE param_name IN (
        '吸气压力-U11', '吸气压力-U12', '吸气压力-U21', '吸气压力-U22',
        '高压压力-U11', '高压压力-U12', '高压压力-U21', '高压压力-U22',
        '新风温度-U1', '新风温度-U2', '回风温度-U1', '回风温度-U2',
        '送风温度-U11', '送风温度-U12', '送风温度-U21', '送风温度-U22',
        '空气质量-CO2-U1', '空气质量-CO2-U2', '空气质量-湿度-U1', '空气质量-湿度-U2',
        '车厢温度-1', '车厢温度-2','车厢湿度-1', '车厢湿度-2'
    )
    ORDER BY msg_calc_parse_time DESC
    LIMIT 5000)  -- dev表取最新5000条

    UNION ALL

    (SELECT
        dvc_train_no,
        dvc_carriage_no,
        param_name,
        param_value,
        msg_calc_dvc_time AS msg_time  -- pro表的时间字段
    FROM pro_param_transposed
    WHERE param_name IN (
        '吸气压力-U11', '吸气压力-U12', '吸气压力-U21', '吸气压力-U22',
        '高压压力-U11', '高压压力-U12', '高压压力-U21', '高压压力-U22',
        '新风温度-U1', '新风温度-U2', '回风温度-U1', '回风温度-U2',
        '送风温度-U11', '送风温度-U12', '送风温度-U21', '送风温度-U22',
        '空气质量-CO2-U1', '空气质量-CO2-U2', '空气质量-湿度-U1', '空气质量-湿度-U2',
        '车厢温度-1', '车厢温度-2','车厢湿度-1', '车厢湿度-2'
    )
    ORDER BY msg_calc_dvc_time DESC
    LIMIT 5000)  -- pro表取最新5000条
)
SELECT
    dvc_train_no,
    dvc_carriage_no,
    MAX(CASE WHEN param_name = '吸气压力-U11' THEN param_value END) AS 吸气压力_U11,
    MAX(CASE WHEN param_name = '吸气压力-U12' THEN param_value END) AS 吸气压力_U12,
    MAX(CASE WHEN param_name = '吸气压力-U21' THEN param_value END) AS 吸气压力_U21,
    MAX(CASE WHEN param_name = '吸气压力-U22' THEN param_value END) AS 吸气压力_U22,
    MAX(CASE WHEN param_name = '高压压力-U11' THEN param_value END) AS 高压压力_U11,
    MAX(CASE WHEN param_name = '高压压力-U12' THEN param_value END) AS 高压压力_U12,
    MAX(CASE WHEN param_name = '高压压力-U21' THEN param_value END) AS 高压压力_U21,
    MAX(CASE WHEN param_name = '高压压力-U22' THEN param_value END) AS 高压压力_U22,
    MAX(CASE WHEN param_name = '新风温度-U1' THEN param_value END) AS 新风温度_U1,
    MAX(CASE WHEN param_name = '新风温度-U2' THEN param_value END) AS 新风温度_U2,
    MAX(CASE WHEN param_name = '回风温度-U1' THEN param_value END) AS 回风温度_U1,
    MAX(CASE WHEN param_name = '回风温度-U2' THEN param_value END) AS 回风温度_U2,
    MAX(CASE WHEN param_name = '送风温度-U11' THEN param_value END) AS 送风温度_U11,
    MAX(CASE WHEN param_name = '送风温度-U12' THEN param_value END) AS 送风温度_U12,
    MAX(CASE WHEN param_name = '送风温度-U21' THEN param_value END) AS 送风温度_U21,
    MAX(CASE WHEN param_name = '送风温度-U22' THEN param_value END) AS 送风温度_U22,
    (COALESCE(MAX(CASE WHEN param_name = '送风温度-U11' THEN param_value END), 0) +
     COALESCE(MAX(CASE WHEN param_name = '送风温度-U12' THEN param_value END), 0)) / 2 AS 送风温度_U1,
    (COALESCE(MAX(CASE WHEN param_name = '送风温度-U21' THEN param_value END), 0) +
     COALESCE(MAX(CASE WHEN param_name = '送风温度-U22' THEN param_value END), 0)) / 2 AS 送风温度_U2,
    MAX(CASE WHEN param_name = '空气质量-CO2-U1' THEN param_value END) AS CO2_U1,
    MAX(CASE WHEN param_name = '空气质量-CO2-U2' THEN param_value END) AS CO2_U2,
    MAX(CASE WHEN param_name = '空气质量-湿度-U1' THEN param_value END) AS 湿度_U1,
    MAX(CASE WHEN param_name = '空气质量-湿度-U2' THEN param_value END) AS 湿度_U2,
    MAX(CASE WHEN param_name = '车厢温度-1' THEN param_value END) AS 车厢温度_1,
    MAX(CASE WHEN param_name = '车厢温度-2' THEN param_value END) AS 车厢温度_2,
    MAX(CASE WHEN param_name = '车厢湿度-1' THEN param_value END) AS 车厢湿度_1,
    MAX(CASE WHEN param_name = '车厢湿度-2' THEN param_value END) AS 车厢湿度_2
FROM latest_records
GROUP BY dvc_train_no, dvc_carriage_no
ORDER BY dvc_train_no, dvc_carriage_no;