CREATE OR REPLACE VIEW chart_line_health_status_count AS
WITH device_status AS (
         SELECT combined_health_data.msg_calc_dvc_no,
            combined_health_data.dvc_train_no,
                CASE
                    WHEN count(*) FILTER (WHERE combined_health_data.health_status <> '健康'::text) = 0 THEN '健康'::text
                    WHEN count(*) FILTER (WHERE combined_health_data.health_status = '非健康'::text) > 0 THEN '非健康'::text
                    ELSE '亚健康'::text
                END AS device_health_status
           FROM ( SELECT dev_view_health_equipment_mat.msg_calc_dvc_no,
                    dev_view_health_equipment_mat.dvc_train_no,
                    dev_view_health_equipment_mat.health_status
                   FROM dev_view_health_equipment_mat
                UNION ALL
                 SELECT pro_view_health_equipment_mat.msg_calc_dvc_no,
                    pro_view_health_equipment_mat.dvc_train_no,
                    pro_view_health_equipment_mat.health_status
                   FROM pro_view_health_equipment_mat) combined_health_data
          GROUP BY combined_health_data.msg_calc_dvc_no, combined_health_data.dvc_train_no
        ), union_data AS (
         SELECT device_status.dvc_train_no,
            '健康'::text AS device_health_status,
            COALESCE(sum(
                CASE
                    WHEN device_status.device_health_status = '健康'::text THEN 1
                    ELSE 0
                END), 0::bigint) AS device_count,
            1 AS health_order
           FROM device_status
          GROUP BY device_status.dvc_train_no
        UNION ALL
         SELECT device_status.dvc_train_no,
            '亚健康'::text AS device_health_status,
            COALESCE(sum(
                CASE
                    WHEN device_status.device_health_status = '亚健康'::text THEN 1
                    ELSE 0
                END), 0::bigint) AS device_count,
            2 AS health_order
           FROM device_status
          GROUP BY device_status.dvc_train_no
        UNION ALL
         SELECT device_status.dvc_train_no,
            '非健康'::text AS device_health_status,
            COALESCE(sum(
                CASE
                    WHEN device_status.device_health_status = '非健康'::text THEN 1
                    ELSE 0
                END), 0::bigint) AS device_count,
            3 AS health_order
           FROM device_status
          GROUP BY device_status.dvc_train_no
        )
 SELECT union_data.dvc_train_no,
    union_data.device_health_status,
    union_data.device_count
   FROM union_data
  ORDER BY union_data.dvc_train_no, union_data.health_order;