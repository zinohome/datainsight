-- public.c_chart_line_fault_type source

CREATE OR REPLACE VIEW public.c_chart_line_fault_type
AS SELECT ft_statistics.line_id::numeric AS dvc_train_no,
    '故障'::text AS "故障类型",
    ft_statistics.alarm_count AS "故障数量",
    'table'::text AS data_source
   FROM ft_statistics
UNION ALL
 SELECT ft_statistics.line_id::numeric AS dvc_train_no,
    '预警'::text AS "故障类型",
    ft_statistics.predict_count AS "故障数量",
    'table'::text AS data_source
   FROM ft_statistics
UNION ALL
 SELECT chart_line_fault_type.dvc_train_no,
    chart_line_fault_type."故障类型",
    chart_line_fault_type."故障数量",
    'view'::text AS data_source
   FROM chart_line_fault_type;