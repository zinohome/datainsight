CREATE OR REPLACE VIEW c_chart_carriage_base AS
SELECT
    dvc_train_no,
    dvc_carriage_no,
    运行模式,
    目标温度,
    新风温度,
    回风温度,
    'table' AS data_source
FROM (
    SELECT
        dvc_train_no,
        dvc_carriage_no,
        运行模式,
        目标温度,
        新风温度,
        回风温度,
        ROW_NUMBER() OVER (PARTITION BY dvc_train_no, dvc_carriage_no ORDER BY report_time DESC) AS rn
    FROM n_chart_carriage_base
) AS t
WHERE t.rn = 1

UNION ALL

SELECT
    dvc_train_no,
    dvc_carriage_no,
    运行模式,
    目标温度,
    新风温度,
    回风温度,
    'view' AS data_source
FROM chart_carriage_base;