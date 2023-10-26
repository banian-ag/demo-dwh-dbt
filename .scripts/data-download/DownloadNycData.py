"""
This script downloads New York City taxi trip record data from the NYC Taxi & Limousine Commission website.
The data is available for each month from 2009 to the current year.
The script reads configuration from a `config.json` file located in the `.scripts` directory.
The configuration specifies the download folder, the base URL for the data files, and the file name prefix and extension.
The script downloads the data files for each month in the specified range and saves them to the download folder.
The script also downloads metadata files for the taxi zones and shapes.
The metadata files are saved to a separate folder specified in the configuration.
Further information can be found her:
    - data page: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    - terms of usage page: https://www.nyc.gov/home/terms-of-use.page
"""
from requests import get
from os import path, makedirs, getcwd
import json
import logging


class DownloadNycData:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def run(self):
        config = self._get_config()
        download_urls = self._get_download_urls(config)
        self._download_files(config["download_folder"], download_urls)
        self._download_files(config["meta_data_folder"], config["meta_data_file_urls"])

    def _get_download_urls(self, config: dict) -> list[str]:
        download_urls = []
        for current_year in range(config["min_year"], config["max_year"] + 1):
            for current_month in range(config["min_month"], 12 + 1):
                file_name = f"{config['file_prefix']}{current_year}-{current_month:02}.{config['file_extension']}"
                url = config["base_url"] + file_name
                download_urls.append(url)
                if (
                    current_year == config["max_year"]
                    and current_month == config["max_month"]
                ):
                    break
        return download_urls

    def _download_files(self, download_folder: str, download_urls: list[str]):
        # create folder if not exists
        if not path.exists(download_folder):
            self.log.info(f"creating folder '{download_folder}'")
            makedirs(download_folder)
        for url in download_urls:
            file_name = url.split("/")[-1]
            target_file = f"{download_folder}{file_name}"
            if not path.exists(target_file):
                self.log.info(f"downloading file '{target_file}'")
                with open(f"{download_folder}{file_name}", "wb") as file:
                    response = get(url)
                    file.write(response.content)
            else:
                self.log.info(f"file '{target_file}' already exists")

    def _get_config(self):
        config_file = path.join(getcwd(), ".scripts", "config.json")
        if not path.exists(config_file):
            raise FileNotFoundError(f"config file not found at '{config_file}'")
        config = None
        with open(config_file, "r") as file:
            config = json.load(file)
        config = config["DownloadNycData"]
        self.log.info(f"using config: {config}")
        return config


if __name__ == "__main__":
    # default logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    instance = DownloadNycData()
    instance.run()
