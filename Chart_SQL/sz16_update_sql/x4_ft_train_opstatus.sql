-- public.ft_train_opstatus definition

-- Drop table

-- DROP TABLE public.ft_train_opstatus;

CREATE TABLE public.ft_train_opstatus (
	id serial4 NOT NULL,
	dvc_train_no int4 NOT NULL,
	latest_op_condition int4 NOT NULL,
	latest_time timestamp NOT NULL,
	immediate_repair int4 NOT NULL,
	enhanced_tracking int4 NOT NULL,
	planned_repair int4 NOT NULL,
	normal_operation int4 NOT NULL,
	send_time timestamp NOT NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT ft_train_opstatus_dvc_train_no_key UNIQUE (dvc_train_no),
	CONSTRAINT ft_train_opstatus_latest_op_condition_check CHECK ((latest_op_condition = ANY (ARRAY[0, 1, 2]))),
	CONSTRAINT ft_train_opstatus_pkey PRIMARY KEY (id),
	CONSTRAINT ft_train_opstatus_正常运营_check CHECK ((normal_operation = ANY (ARRAY[0, 1])))
);

-- Table Triggers

create trigger update_fault_records_timestamp before
update
    on
    public.ft_train_opstatus for each row execute function update_timestamp();
create trigger update_train_status_timestamp before
update
    on
    public.ft_train_opstatus for each row execute function update_timestamp();