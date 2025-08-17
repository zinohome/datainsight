CREATE OR REPLACE VIEW chart_health_equipment AS
SELECT
	dvc_train_no as 车号,
	dvc_carriage_no as 车厢号,
	param_name as 部件,
	life_ratio as 耗用率,
	baseline_data as 额定寿命,
	param_value as 已耗
FROM public.dev_view_health_equipment_mat

union all

SELECT
	dvc_train_no as 车号,
	dvc_carriage_no as 车厢号,
	param_name as 部件,
	life_ratio as 耗用率,
	baseline_data as 额定寿命,
	param_value as 已耗
FROM public.pro_view_health_equipment_mat

order by 车号, 车厢号,耗用率 desc
