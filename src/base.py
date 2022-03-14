import pathlib
import configparser
import logging


# PATHS
ROOT = pathlib.Path(__file__).parent.parent
CONFIG = f'{ROOT}/data/parameter.cfg'


# LOG
logger = logging.getLogger(__name__)



class Parameters:
    """ Read and parse configuration """
    def __init__(self):
        # Parse configuration
        try:
            self._parseConfig(CONFIG)
        except FileNotFoundError:
            print(f"{CONFIG} file not found")
            raise

    def _parseConfig(self, config_file: str) -> None:
        parser = configparser.ConfigParser()
        parser.read_file(open(config_file))
        self.telegram_bot_token = parser.get("TOKENS", "telegram_bot")
        self.open_weather_token = parser.get("TOKENS", "openweather")
