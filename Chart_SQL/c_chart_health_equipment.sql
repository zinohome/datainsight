CREATE OR REPLACE VIEW c_chart_health_equipment AS
WITH base_data AS (
    SELECT t."车号",
        t."车厢号",
        t."部件",
        t."额定寿命",
        t."已耗" AS original_已耗,
        t.report_time,
        t.data_source
    FROM (
        SELECT n_chart_health_equipment."车号",
            n_chart_health_equipment."车厢号",
            n_chart_health_equipment."部件",
            n_chart_health_equipment."额定寿命",
            n_chart_health_equipment."已耗",
            n_chart_health_equipment.report_time,
            'table'::text AS data_source,
            row_number() OVER (PARTITION BY n_chart_health_equipment."车号", n_chart_health_equipment."车厢号", n_chart_health_equipment."部件" ORDER BY n_chart_health_equipment.report_time DESC) AS rn
        FROM n_chart_health_equipment
    ) t
    WHERE t.rn = 1
    UNION ALL
    SELECT chart_health_equipment."车号",
        chart_health_equipment."车厢号",
        chart_health_equipment."部件",
        chart_health_equipment."额定寿命",
        chart_health_equipment."已耗",
        NULL::timestamp without time zone AS report_time,
        'view'::text AS data_source
    FROM chart_health_equipment
),
clean_data AS (
    SELECT "车号",
        "车厢号",
        "部件",
        SUM("已耗") AS total_cleaned_已耗
    FROM d_chart_health_clean
    GROUP BY "车号", "车厢号", "部件"
)
SELECT base_data."车号",
    base_data."车厢号",
    base_data."部件",
    CAST(CASE 
        WHEN base_data."额定寿命" > 0 THEN 
            CASE 
                WHEN base_data."额定寿命" IN (50000, 25000) THEN 
                    ((base_data.original_已耗 - COALESCE(clean_data.total_cleaned_已耗, 0)) / 3600) / base_data."额定寿命"
                ELSE 
                    (base_data.original_已耗 - COALESCE(clean_data.total_cleaned_已耗, 0)) / base_data."额定寿命"
            END
        ELSE 0
    END AS numeric) AS "耗用率",
    base_data."额定寿命",
    (base_data.original_已耗 - COALESCE(clean_data.total_cleaned_已耗, 0)) AS "已耗",
    base_data.report_time,
    base_data.data_source
FROM base_data
LEFT JOIN clean_data
    ON base_data."车号" = clean_data."车号"
    AND base_data."车厢号" = clean_data."车厢号"
    AND base_data."部件" = clean_data."部件"
ORDER BY 1, 2, 4 DESC;