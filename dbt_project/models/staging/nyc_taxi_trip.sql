/*
    details see:
    https://learn.microsoft.com/en-us/azure/open-datasets/dataset-taxi-yellow?tabs=azureml-opendatasets
*/
select * from {{ source("raw_data", "nyc_yellow_taxi_trip") }}