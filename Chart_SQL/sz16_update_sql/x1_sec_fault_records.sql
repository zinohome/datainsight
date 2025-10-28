-- public.sec_fault_records definition

-- Drop table

-- DROP TABLE public.sec_fault_records;

CREATE TABLE public.sec_fault_records (
	msg_calc_dvc_no text NOT NULL,
	fault_name text NOT NULL,
	msg_calc_train_no text NULL,
	dvc_train_no int4 NULL,
	dvc_carriage_no int4 NULL,
	start_time timestamptz NULL,
	end_time timestamptz NULL,
	update_time timestamptz NOT NULL,
	status text NULL,
	fault_level text NULL,
	repair_suggestion text NULL,
	fault_type text NULL,
	CONSTRAINT sec_fault_records_pkey PRIMARY KEY (msg_calc_dvc_no, fault_name)
);
CREATE INDEX idx_sec_fault_key_time ON public.sec_fault_records USING btree (msg_calc_dvc_no, fault_name, update_time DESC);