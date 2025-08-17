CREATE OR REPLACE VIEW c_chart_carriage_param AS
SELECT
    dvc_train_no,
    dvc_carriage_no,
    吸气压力_U11,
    吸气压力_U12,
    吸气压力_U21,
    吸气压力_U22,
    高压压力_U11,
    高压压力_U12,
    高压压力_U21,
    高压压力_U22,
    新风温度_U1,
    新风温度_U2,
    回风温度_U1,
    回风温度_U2,
    送风温度_U11,
    送风温度_U12,
    送风温度_U21,
    送风温度_U22,
    送风温度_U1,
    送风温度_U2,
    CO2_U1,
    CO2_U2,
    湿度_U1,
    湿度_U2,
    车厢温度_1,
    车厢温度_2,
    车厢湿度_1,
    车厢湿度_2,
    report_time,
    data_source
FROM (
    -- 从n_chart_carriage_param表获取最新数据
    SELECT
        dvc_train_no,
        dvc_carriage_no,
        吸气压力_U11,
        吸气压力_U12,
        吸气压力_U21,
        吸气压力_U22,
        高压压力_U11,
        高压压力_U12,
        高压压力_U21,
        高压压力_U22,
        新风温度_U1,
        新风温度_U2,
        回风温度_U1,
        回风温度_U2,
        送风温度_U11,
        送风温度_U12,
        送风温度_U21,
        送风温度_U22,
        送风温度_U1,
        送风温度_U2,
        CO2_U1,
        CO2_U2,
        湿度_U1,
        湿度_U2,
        车厢温度_1,
        车厢温度_2,
        车厢湿度_1,
        车厢湿度_2,
        report_time,
        'table' AS data_source
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY dvc_train_no, dvc_carriage_no ORDER BY report_time DESC) AS rn
        FROM n_chart_carriage_param
    ) AS t
    WHERE t.rn = 1

    UNION ALL

    -- 从chart_carriage_param视图获取数据
    SELECT
        dvc_train_no,
        dvc_carriage_no,
        吸气压力_U11,
        吸气压力_U12,
        吸气压力_U21,
        吸气压力_U22,
        高压压力_U11,
        高压压力_U12,
        高压压力_U21,
        高压压力_U22,
        新风温度_U1,
        新风温度_U2,
        回风温度_U1,
        回风温度_U2,
        送风温度_U11,
        送风温度_U12,
        送风温度_U21,
        送风温度_U22,
        送风温度_U1,
        送风温度_U2,
        CO2_U1,
        CO2_U2,
        湿度_U1,
        湿度_U2,
        车厢温度_1,
        车厢温度_2,
        车厢湿度_1,
        车厢湿度_2,
        NULL AS report_time,
        'view' AS data_source
    FROM chart_carriage_param
) AS combined_data;