-- public.c_chart_view_train_opstatus source

CREATE OR REPLACE VIEW public.c_chart_view_train_opstatus
AS SELECT ft_train_opstatus.dvc_train_no,
    ft_train_opstatus.latest_op_condition,
    ft_train_opstatus.latest_time,
    ft_train_opstatus.immediate_repair AS "立即维修",
    ft_train_opstatus.enhanced_tracking AS "加强跟踪",
    ft_train_opstatus.planned_repair AS "计划维修",
    ft_train_opstatus.normal_operation AS "正常运营",
    'table'::text AS data_source
   FROM ft_train_opstatus
UNION ALL
 SELECT chart_view_train_opstatus.dvc_train_no,
    chart_view_train_opstatus.latest_op_condition,
    chart_view_train_opstatus.latest_time,
    chart_view_train_opstatus."立即维修",
    chart_view_train_opstatus."加强跟踪",
    chart_view_train_opstatus."计划维修",
    chart_view_train_opstatus."正常运营",
    'view'::text AS data_source
   FROM chart_view_train_opstatus;