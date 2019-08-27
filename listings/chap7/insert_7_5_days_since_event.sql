
INSERT into metric_name values (NEW_ID,concat('days_since_event_to_query' ))
ON CONFLICT DO NOTHING;


with date_vals AS (
  select i::date as metric_date
	from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '7 day'::interval) i
),
last_event as (
    select account_id, metric_date, max(event_time)::date as last_date
    from event e inner join date_vals d
    on e.event_time::date <= metric_date
    inner join event_type t on t.event_type_id=e.event_type_id
    where t.event_type_name='event_to_query'
    group by account_id, metric_date
    order by account_id, metric_date
)

insert into metric (account_id,metric_time,metric_name_id,metric_value)

select account_id, metric_date, NEW_ID,
metric_date - last_date as days_since_event
from last_event
ON CONFLICT DO NOTHING;
