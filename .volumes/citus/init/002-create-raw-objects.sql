create schema if not exists raw_data;
drop table if exists raw_data.nyc_yellow_taxi_trip;
CREATE TABLE raw_data.nyc_yellow_taxi_trip (
	vendorid float8 NULL,
	tpep_pickup_datetime timestamp NULL,
	tpep_dropoff_datetime timestamp NULL,
	passenger_count float8 NULL,
	trip_distance float8 NULL,
	ratecodeid float8 NULL,
	store_and_fwd_flag varchar(20) NULL,
	pulocationid float8 NULL,
	dolocationid float8 NULL,
	payment_type float8 NULL,
	fare_amount float8 NULL,
	extra float8 NULL,
	mta_tax float8 NULL,
	tip_amount float8 NULL,
	tolls_amount float8 NULL,
	improvement_surcharge float8 NULL,
	total_amount float8 NULL,
	congestion_surcharge float8 NULL,
	airport_fee float8 NULL,
	meta_row_number int8 NOT NULL,
	meta_file_name varchar(100) NOT NULL
);
select alter_table_set_access_method('raw_data.nyc_yellow_taxi_trip', 'columnar');
select create_distributed_table('raw_data.nyc_yellow_taxi_trip', 'vendor_name');