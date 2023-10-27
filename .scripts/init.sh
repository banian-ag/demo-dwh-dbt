#!/bin/bash

# Parse command line arguments
while [ "$1" != "" ]; do
    case $1 in
        --remove ) remove=1
                   ;;
        * )       echo "Invalid argument: $1"
                   exit 1
    esac
    shift
done

####################################################################
# Initialize virtual environment and install dependencies
####################################################################
echo "Initializing virtual environment and installing dependencies..." 
if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
source .venv/Scripts/Activate
pip install -r requirements.txt
echo "...done!" 

####################################################################
# Download data files
####################################################################
echo "Downloading data files..." 
python3 ./.scripts/data-download/DownloadNycData.py
echo "...done!" 

####################################################################
# Remove volumes folders
####################################################################
if [ "$remove" ]; then
    echo "Removing volumes..." 
    if [ -d ./.volumes/citus/data-master ]; then
        rm -rf ./.volumes/citus/data-master
    fi
    if [ -d ./.volumes/citus/data-worker ]; then
        rm -rf ./.volumes/citus/data-worker
    fi
    echo "...done!" 
fi

####################################################################
# Create volumes folders
####################################################################
echo "Creating volumes folders..." 
if [ ! -d ./.volumes/citus/data-master ]; then
    mkdir ./.volumes/citus/data-master
fi
if [ ! -d ./.volumes/citus/data-worker ]; then
    mkdir ./.volumes/citus/data-worker
fi
if [ ! -d ./.volumes/citus/init ]; then
    mkdir ./.volumes/citus/init
fi
echo "...done!" 

####################################################################
# Create local env file
####################################################################
echo "Creating local env file..." 
python3 ./.scripts/docker-env/BuildLocalEnvFile.py
echo "...done!" 

####################################################################
# Start docker compose
####################################################################
echo "Starting docker compose..." 
# as a preventive measure, remove all containers
docker compose down
docker compose --env-file .env.local up -d
echo "...done!" 

####################################################################
# Load the raw data
####################################################################
echo "Start data load..." 
sleep 20
python3 ./.scripts/data-load/LoadNycData.py
echo "...done!"
