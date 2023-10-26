"""
This script loads data from parquet files into a PostgreSQL database. It expects a configuration file in JSON format
to be present in the `.scripts` directory. The configuration file should specify the location of the data files, the
database connection details, and other parameters such as batch size. The script reads the configuration file, finds
all parquet files in the specified directory, and loads them into the specified database table in batches. The script
logs progress and errors to the console using the Python logging module.
"""
from os import path, getcwd, listdir
import json
import logging
import pandas as pd
from sqlalchemy import create_engine


class LoadNycData:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def run(self):
        config = self._get_config()
        data_files = self._get_data_files(config)
        self._load_data_files(config, data_files)

    def _get_data_files(self, config: dict) -> list[str]:
        data_files = []
        data_folder = config["DownloadNycData"]["download_folder"]
        file_prefix = config["DownloadNycData"]["file_prefix"]
        file_extension = config["DownloadNycData"]["file_extension"]
        for file_name in listdir(data_folder):
            if file_name.startswith(file_prefix) and file_name.endswith(file_extension):
                data_files.append(path.join(data_folder, file_name))
        return data_files

    def _load_data_files(self, config: dict, data_files: list[str]):
        db_url = f"postgresql+psycopg2://{config['CitusDwhConfig']['user']}:{config['CitusDwhConfig']['password']}@{config['CitusDwhConfig']['host']}:{config['CitusDwhConfig']['port']}/{config['CitusDwhConfig']['dbname']}"
        engine = create_engine(db_url)
        for data_file in data_files:
            self.log.info(
                f"loading data from '{data_file}' to '{config['LoadNycData']['schema_name']}.{config['LoadNycData']['table_name']}'"
            )
            df = pd.read_parquet(data_file)
            df.columns = df.columns.str.lower()
            df["file_name"] = data_file
            self.log.info(f"loaded {len(df)} rows from file '{data_file}'")
            for i in range(0, len(df), config["LoadNycData"]["batch_size"]):
                chunk = df[i : i + config["LoadNycData"]["batch_size"]]
                chunk.to_sql(
                    config["LoadNycData"]["table_name"],
                    engine,
                    if_exists="append",
                    index=False,
                    schema=config["LoadNycData"]["schema_name"],
                )
                self.log.info(
                    f"loaded {((i+config['LoadNycData']['batch_size'])/len(df)*100):.2f}% of file '{data_file}'"
                )

    def _get_config(self) -> dict:
        config_file = path.join(getcwd(), ".scripts", "config.json")
        if not path.exists(config_file):
            raise FileNotFoundError(f"config file not found at '{config_file}'")
        config = None
        with open(config_file, "r") as file:
            config = json.load(file)
        self.log.info(f"using config: {config}")
        return config


if __name__ == "__main__":
    # default logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    instance = LoadNycData()
    instance.run()
