create schema if not exists raw_data;
drop table if exists raw_data.nyc_yellow_taxi_trip;
create table raw_data.nyc_yellow_taxi_trip (
	vendor_name varchar(50) NULL,
	trip_pickup_datetime varchar(20) NULL,
	trip_dropoff_datetime varchar(20) NULL,
	passenger_count int8 NULL,
	trip_distance float8 NULL,
	start_lon float8 NULL,
	start_lat float8 NULL,
	rate_code float8 NULL,
	store_and_forward float8 NULL,
	end_lon float8 NULL,
	end_lat float8 NULL,
	payment_type varchar(20) NULL,
	fare_amt float8 NULL,
	surcharge float8 NULL,
	mta_tax float8 NULL,
	tip_amt float8 NULL,
	tolls_amt float8 NULL,
	total_amt float8 NULL,
	file_name varchar(100) NOT NULL
);
select alter_table_set_access_method('raw_data.nyc_yellow_taxi_trip', 'columnar');
select create_distributed_table('raw_data.nyc_yellow_taxi_trip', 'vendor_name');