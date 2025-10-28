-- public.chart_view_train_opstatus source

CREATE OR REPLACE VIEW public.chart_view_train_opstatus
AS SELECT combined_data.dvc_train_no,
    max(combined_data.latest_op_condition) AS latest_op_condition,
    max(combined_data.latest_time) AS latest_time,
    sum(combined_data."立即维修") AS "立即维修",
    sum(combined_data."加强跟踪") AS "加强跟踪",
    sum(combined_data."计划维修") AS "计划维修",
    sum(combined_data."正常运营") AS "正常运营"
   FROM chart_view_train_opstatus_daily combined_data
  GROUP BY combined_data.dvc_train_no
  ORDER BY combined_data.dvc_train_no;