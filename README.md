# Documentation

## Introduction

## Pre-requisites

You either need a windows or a linux machine to run this project. You also need to have python3, docker and docker-compose installed on your machine.

sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt-get install libpq-dev
sudo apt install python3.10-venv

dbt-init --client banian_ag --warehouse postgres --target_dir ./ --project_name demo_dwh_dbt --project_directory dbt-project
