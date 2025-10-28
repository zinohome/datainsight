-- public.ft_statistics definition

-- Drop table

-- DROP TABLE public.ft_statistics;

CREATE TABLE public.ft_statistics (
	id bigserial NOT NULL,
	line_id varchar(10) NOT NULL,
	send_time timestamp NOT NULL,
	alarm_count int4 NOT NULL,
	predict_count int4 NOT NULL,
	health_count int4 NOT NULL,
	limit_health_count int4 NOT NULL,
	not_health_count int4 NOT NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT ft_statistics_alarm_count_check CHECK ((alarm_count >= 0)),
	CONSTRAINT ft_statistics_health_count_check CHECK ((health_count >= 0)),
	CONSTRAINT ft_statistics_limit_health_count_check CHECK ((limit_health_count >= 0)),
	CONSTRAINT ft_statistics_not_health_count_check CHECK ((not_health_count >= 0)),
	CONSTRAINT ft_statistics_pkey PRIMARY KEY (id),
	CONSTRAINT ft_statistics_predict_count_check CHECK ((predict_count >= 0))
);

-- Table Triggers

create trigger update_ft_statistics_timestamp before
update
    on
    public.ft_statistics for each row execute function update_timestamp();