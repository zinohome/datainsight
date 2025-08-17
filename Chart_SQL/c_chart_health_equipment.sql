CREATE OR REPLACE VIEW c_chart_health_equipment AS
 SELECT t."车号",
    t."车厢号",
    t."部件",
    t."耗用率",
    t."额定寿命",
    t."已耗",
    t.report_time,
    'table'::text AS data_source
   FROM ( SELECT n_chart_health_equipment."车号",
            n_chart_health_equipment."车厢号",
            n_chart_health_equipment."部件",
            n_chart_health_equipment."耗用率",
            n_chart_health_equipment."额定寿命",
            n_chart_health_equipment."已耗",
            n_chart_health_equipment.report_time,
            row_number() OVER (PARTITION BY n_chart_health_equipment."车号", n_chart_health_equipment."车厢号", n_chart_health_equipment."部件" ORDER BY n_chart_health_equipment.report_time DESC) AS rn
           FROM n_chart_health_equipment) t
  WHERE t.rn = 1
UNION ALL
 SELECT chart_health_equipment."车号",
    chart_health_equipment."车厢号",
    chart_health_equipment."部件",
    chart_health_equipment."耗用率",
    chart_health_equipment."额定寿命",
    chart_health_equipment."已耗",
    NULL::timestamp without time zone AS report_time,
    'view'::text AS data_source
   FROM chart_health_equipment
  ORDER BY 1, 2, 4 DESC;