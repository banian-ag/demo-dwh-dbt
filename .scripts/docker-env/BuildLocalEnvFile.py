from os import path, makedirs, getcwd, listdir
import json
import logging


class LoadNycData:
    key_replacements = {
        "CITUS_POSTGRES_USER": "user",
        "CITUS_POSTGRES_PASSWORD": "password",
    }

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def run(self):
        config = self._get_config()
        self._build_local_env_file(config)

    def _build_local_env_file(self, config: dict):
        env_file = path.join(getcwd(), ".env.template")
        local_env_file = path.join(getcwd(), ".env.local")
        with open(env_file, "r") as file, open(local_env_file, "w") as local_file:
            for line in file.readlines():
                if line.startswith("#"):
                    local_file.write(line)
                    continue
                key = line.split("=")[0]
                if key in self.key_replacements:
                    value = config["CitusDwhConfig"][self.key_replacements[key]]
                    local_file.write(f"{key}={value}\n")
                    self.log.info(f"replaced '{key}' with '{value}'")
                else:
                    local_file.write(line)

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
