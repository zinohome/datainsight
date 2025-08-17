CREATE OR REPLACE VIEW chart_carriage_param_current AS
WITH latest_data AS (
        -- dev表取最新5000条
        (SELECT
            dvc_train_no,
            dvc_carriage_no,
            param_name,
            param_value,
            msg_calc_parse_time AS msg_time  -- dev表时间字段
        FROM dev_param_transposed
        WHERE param_name IN (
            '通风机电流-U11', '压缩机电流-U11', '冷凝风机电流-U11',
            '通风机电流-U12', '压缩机电流-U12', '冷凝风机电流-U12',
            '通风机电流-U21', '压缩机电流-U21', '冷凝风机电流-U21',
            '通风机电流-U22', '压缩机电流-U22', '冷凝风机电流-U22'
        )
        ORDER BY msg_time DESC
        LIMIT 5000)

        UNION ALL

        -- pro表取最新5000条
        (SELECT
            dvc_train_no,
            dvc_carriage_no,
            param_name,
            param_value,
            msg_calc_dvc_time AS msg_time  -- pro表时间字段
        FROM pro_param_transposed
        WHERE param_name IN (
            '通风机电流-U11', '压缩机电流-U11', '冷凝风机电流-U11',
            '通风机电流-U12', '压缩机电流-U12', '冷凝风机电流-U12',
            '通风机电流-U21', '压缩机电流-U21', '冷凝风机电流-U21',
            '通风机电流-U22', '压缩机电流-U22', '冷凝风机电流-U22'
        )
        ORDER BY msg_time DESC
        LIMIT 5000)
    )
SELECT DISTINCT ON (dvc_train_no, param_name)
    dvc_train_no,
    dvc_carriage_no,
    param_name,
    param_value
FROM latest_data
ORDER BY dvc_train_no, param_name, msg_time DESC;