-- public.c_chart_view_fault_timed source

CREATE OR REPLACE VIEW public.c_chart_view_fault_timed
AS SELECT ft_fault_records.msg_calc_dvc_no::text AS msg_calc_dvc_no,
    '0'::text AS msg_calc_train_no,
    0 AS dvc_train_no,
    0 AS dvc_carriage_no,
    ft_fault_records.fault_name,
    ft_fault_records.start_time,
    ft_fault_records.end_time,
    ft_fault_records.updated_at AS update_time,
    ft_fault_records.status,
    ft_fault_records.fault_level::text AS fault_level,
    ft_fault_records.repair_suggestion,
    ft_fault_records.fault_type,
    'table'::text AS data_source
   FROM ft_fault_records 
UNION ALL 
 SELECT sec_fault_records.msg_calc_dvc_no,
    sec_fault_records.msg_calc_train_no,
    sec_fault_records.dvc_train_no,
    sec_fault_records.dvc_carriage_no,
    sec_fault_records.fault_name,
    sec_fault_records.start_time,
    sec_fault_records.end_time,
    sec_fault_records.update_time,
    sec_fault_records.status,
    sec_fault_records.fault_level,
    sec_fault_records.repair_suggestion,
    sec_fault_records.fault_type,
    'table'::text AS data_source
   FROM sec_fault_records;