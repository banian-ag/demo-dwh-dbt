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
from sqlalchemy.engine import Engine
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading
import psycopg2
from io import StringIO


class LoadNycData:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.inserted_rows = 0
        self.start = datetime.min
        self.lock = threading.Semaphore()

    def run(self):
        config = self._get_config()
        data_files = self._get_data_files(config)
        self._load_data_files(config, data_files)

    def _load_data_files(self, config: dict, data_files: list[str]):
        engine = self._get_engine(config)
        schema_name = config["LoadNycData"]["schema_name"]
        table_name = config["LoadNycData"]["table_name"]
        batch_size = config["LoadNycData"]["batch_size"]
        parallelism = config["LoadNycData"]["parallelism"]
        self.start = datetime.now()
        for i in range(0, len(data_files), parallelism):
            data_file_slice = data_files[i : i + parallelism]
            with ThreadPoolExecutor() as executor:
                futures = []
                for data_file in data_file_slice:
                    futures.append(
                        executor.submit(
                            self._load_data_file,
                            config,
                            data_file,
                            engine,
                            schema_name,
                            table_name,
                            batch_size,
                        )
                    )
                for future in futures:
                    future.result()

    def _load_data_file(
        self,
        config: dict,
        data_file: str,
        engine: Engine,
        schema_name: str,
        table_name: str,
        batch_size: int,
    ):
        self.log.info(
            f"loading data from '{data_file}' to '{schema_name}.{table_name}'"
        )
        df = self._get_data_frame(data_file)
        self.log.info(f"loaded {len(df)} rows from file '{data_file}'")
        for i in range(0, len(df), batch_size):
            chunk = df[i : i + batch_size]
            self._insert_chunk(
                chunk,
                engine,
                schema_name,
                table_name,
            )
            self.log.info(
                f"loaded {((i+batch_size-1)/len(df)*100):.2f}% of file '{data_file}'"
            )

    def _get_data_files(self, config: dict) -> list[str]:
        data_files = []
        data_folder = config["LoadNycData"]["load_folder"]
        file_prefix = config["DownloadNycData"]["file_prefix"]
        file_extension = config["DownloadNycData"]["file_extension"]
        for file_name in listdir(data_folder):
            if file_name.startswith(file_prefix) and file_name.endswith(file_extension):
                data_files.append(path.join(data_folder, file_name))
        return data_files

    def _get_config(self) -> dict:
        config_file = path.join(getcwd(), ".scripts", "config.json")
        if not path.exists(config_file):
            raise FileNotFoundError(f"config file not found at '{config_file}'")
        config = None
        with open(config_file, "r") as file:
            config = json.load(file)
        self.log.info(f"using config: {config}")
        return config

    def _get_engine(self, config: dict) -> Engine:
        db_url = f"postgresql+psycopg2://{config['CitusDwhConfig']['user']}:{config['CitusDwhConfig']['password']}@{config['CitusDwhConfig']['host']}:{config['CitusDwhConfig']['port']}/{config['CitusDwhConfig']['dbname']}"
        engine = create_engine(db_url)
        return engine

    def _get_data_frame(self, data_file: str) -> pd.DataFrame:
        df = pd.read_parquet(data_file)
        df.columns = df.columns.str.lower()
        # add meta data columns
        df["meta_row_number"] = df.index
        df["meta_file_name"] = path.basename(data_file)

        return df

    def _insert_chunk_old(
        self, chunk: pd.DataFrame, engine: Engine, schema_name: str, table_name: str
    ):
        chunk.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            schema=schema_name,
        )
        self._chunk_added(len(chunk))

    def _insert_chunk(
        self, chunk: pd.DataFrame, engine: Engine, schema_name: str, table_name: str
    ):
        try:
            connection = engine.raw_connection()
            cursor = connection.cursor()

            # Create a CSV representation of the DataFrame
            csv_buffer = StringIO()
            chunk.to_csv(csv_buffer, sep="\t", header=False, index=False)
            csv_buffer.seek(0)

            # Copy data from the CSV buffer to the table
            cursor.copy_expert(
                f"COPY {schema_name}.{table_name} FROM stdin WITH CSV DELIMITER as E'\\t'",
                csv_buffer,
            )

            connection.commit()

            self._chunk_added(len(chunk))

        except (Exception, psycopg2.Error) as error:
            print(f"Error: {error}")
        finally:
            if connection is not None:
                cursor.close()
                connection.close()

    def _chunk_added(self, chunk_size):
        # lock inserted rows
        self.lock.acquire()
        self.inserted_rows += chunk_size
        self.lock.release()
        # log progress
        time_delta = datetime.now() - self.start
        records_per_second = self.inserted_rows / time_delta.total_seconds()
        self.log.info(
            f"inserted {self.inserted_rows} rows in {time_delta.total_seconds():.2f} seconds ({records_per_second:.2f} records per second)"
        )


if __name__ == "__main__":
    # default logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    instance = LoadNycData()
    instance.run()
