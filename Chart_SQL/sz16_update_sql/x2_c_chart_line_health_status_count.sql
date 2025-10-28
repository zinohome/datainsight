-- public.c_chart_line_health_status_count source

CREATE OR REPLACE VIEW public.c_chart_line_health_status_count
AS SELECT ft_statistics.line_id::numeric AS dvc_train_no,
    '健康'::text AS device_health_status,
    ft_statistics.health_count AS device_count,
    'table'::text AS data_source
   FROM ft_statistics
UNION ALL
 SELECT ft_statistics.line_id::numeric AS dvc_train_no,
    '亚健康'::text AS device_health_status,
    ft_statistics.limit_health_count AS device_count,
    'table'::text AS data_source
   FROM ft_statistics
UNION ALL
 SELECT ft_statistics.line_id::numeric AS dvc_train_no,
    '非健康'::text AS device_health_status,
    ft_statistics.not_health_count AS device_count,
    'table'::text AS data_source
   FROM ft_statistics
UNION ALL
 SELECT chart_line_health_status_count.dvc_train_no,
    chart_line_health_status_count.device_health_status,
    chart_line_health_status_count.device_count,
    'view'::text AS data_source
   FROM chart_line_health_status_count;