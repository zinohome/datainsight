-- public.mv_train_latest_condition source

CREATE MATERIALIZED VIEW public.mv_train_latest_condition
TABLESPACE pg_default
AS SELECT DISTINCT ON (pro_macda.dvc_train_no) pro_macda.dvc_train_no,
    pro_macda.dvc_op_condition AS latest_op_condition,
    pro_macda.msg_calc_dvc_time AS latest_time
   FROM pro_macda
  WHERE pro_macda.msg_calc_dvc_time >= (now() - '7 days'::interval)
  ORDER BY pro_macda.dvc_train_no, pro_macda.msg_calc_dvc_time DESC
WITH DATA;

-- View indexes:
CREATE UNIQUE INDEX idx_mv_train_latest_condition_train ON public.mv_train_latest_condition USING btree (dvc_train_no);