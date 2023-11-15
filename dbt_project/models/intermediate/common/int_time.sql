with time_range as
(
	select
        distinct -- to remove double 00:00:00
		x::time as full_time
	from generate_series(timestamp '2000-01-01', timestamp '2000-01-02', interval  '1 second') t(x)
)
select
    full_time,
    extract(hour from full_time) as hour,
    extract(minute from full_time) as minute,
    extract(second from full_time) as second
from time_range