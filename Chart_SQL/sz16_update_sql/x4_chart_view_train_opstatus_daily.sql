-- public.chart_view_train_opstatus_daily source

CREATE OR REPLACE VIEW public.chart_view_train_opstatus_daily
AS WITH unique_trains AS (
         SELECT DISTINCT pro_macda_ac.dvc_train_no
           FROM pro_macda_ac
        ), latest_conditions AS (
         SELECT mv_train_latest_condition.dvc_train_no,
            mv_train_latest_condition.latest_op_condition,
            mv_train_latest_condition.latest_time
           FROM mv_train_latest_condition
        ), fault_stats AS (
         SELECT sec_fault_records.dvc_train_no,
            count(
                CASE
                    WHEN sec_fault_records.fault_type = '故障'::text AND sec_fault_records.status <> '结束'::text THEN 1
                    ELSE NULL::integer
                END) AS immediate_repair_cnt,
            count(
                CASE
                    WHEN sec_fault_records.fault_type = '预警'::text AND sec_fault_records.status <> '结束'::text THEN 1
                    ELSE NULL::integer
                END) AS plan_tracking_cnt
           FROM sec_fault_records
          GROUP BY sec_fault_records.dvc_train_no
        ), health_stats AS (
         SELECT pro_view_health_equipment_mat.dvc_train_no,
            count(
                CASE
                    WHEN pro_view_health_equipment_mat.health_status = '非健康'::text THEN 1
                    ELSE NULL::integer
                END) AS plan_repair_cnt
           FROM pro_view_health_equipment_mat
          GROUP BY pro_view_health_equipment_mat.dvc_train_no
        )
 SELECT ut.dvc_train_no,
    lc.latest_op_condition,
    lc.latest_time,
    COALESCE(fs.immediate_repair_cnt, 0::bigint) AS "立即维修",
    COALESCE(fs.plan_tracking_cnt, 0::bigint) AS "加强跟踪",
    COALESCE(hs.plan_repair_cnt, 0::bigint) AS "计划维修",
        CASE
            WHEN COALESCE(fs.immediate_repair_cnt, 0::bigint) = 0 AND COALESCE(fs.plan_tracking_cnt, 0::bigint) = 0 AND COALESCE(hs.plan_repair_cnt, 0::bigint) = 0 THEN 1
            ELSE 0
        END AS "正常运营"
   FROM unique_trains ut
     LEFT JOIN latest_conditions lc ON ut.dvc_train_no = lc.dvc_train_no
     LEFT JOIN fault_stats fs ON ut.dvc_train_no = fs.dvc_train_no
     LEFT JOIN health_stats hs ON ut.dvc_train_no = hs.dvc_train_no;