-- public.ft_fault_records definition

-- Drop table

-- DROP TABLE public.ft_fault_records;

CREATE TABLE public.ft_fault_records (
	msg_calc_dvc_no int4 NOT NULL,
	fault_name varchar(255) NOT NULL,
	start_time timestamp NOT NULL,
	end_time timestamp NULL,
	status varchar(10) NOT NULL,
	fault_level int4 NOT NULL,
	repair_suggestion text NOT NULL,
	fault_type varchar(10) NOT NULL,
	send_time timestamp NOT NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT check_end_time CHECK (((((status)::text = '结束'::text) AND (end_time IS NOT NULL) AND (end_time > start_time)) OR (((status)::text = '持续'::text) AND (end_time IS NULL)))),
	CONSTRAINT ft_fault_records_fault_level_check CHECK (((fault_level >= 1) AND (fault_level <= 5))),
	CONSTRAINT ft_fault_records_fault_type_check CHECK (((fault_type)::text = ANY ((ARRAY['预警'::character varying, '故障'::character varying])::text[]))),
	CONSTRAINT ft_fault_records_pkey PRIMARY KEY (msg_calc_dvc_no, fault_name, start_time),
	CONSTRAINT ft_fault_records_status_check CHECK (((status)::text = ANY ((ARRAY['持续'::character varying, '结束'::character varying])::text[])))
);