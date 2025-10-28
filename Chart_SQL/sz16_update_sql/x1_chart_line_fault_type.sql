-- public.chart_line_fault_type source

CREATE OR REPLACE VIEW public.chart_line_fault_type
AS SELECT combined.dvc_train_no,
    combined.fault_type AS "故障类型",
    sum(combined."故障数量") AS "故障数量"
   FROM ( SELECT sec_fault_records.dvc_train_no,
            sec_fault_records.fault_type,
            count(*) AS "故障数量"
           FROM sec_fault_records
          WHERE sec_fault_records.status = '持续'::text
          GROUP BY sec_fault_records.dvc_train_no, sec_fault_records.fault_type) combined
  GROUP BY combined.dvc_train_no, combined.fault_type
  ORDER BY combined.fault_type, combined.dvc_train_no;