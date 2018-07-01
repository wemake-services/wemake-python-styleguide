# -*- coding: utf-8 -*-

import configparser
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigFileParser(object):
    """This class parses configs from `setup.cfg` file."""

    CONFIG_FILE_NAME = 'setup.cfg'
    CONFIG_SECTION_NAME = 'wemake_python_styleguide'

    def __init__(self, config_file_path: Optional[str] = None) -> None:
        """Initialize object to find WPS section in config file."""
        default_config_path = BASE_DIR.joinpath(self.CONFIG_FILE_NAME)
        self.config_file_path = config_file_path or default_config_path
        config = configparser.ConfigParser()
        config.read(self.config_file_path)
        self.configs = config[self.CONFIG_SECTION_NAME]

    def get_option(self, option: str) -> int:
        """Returns config option by option's key."""
        config_option = self.configs[option]
        return int(config_option)
