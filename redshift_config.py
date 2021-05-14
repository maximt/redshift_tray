''' redshift settings parser '''

from typing import Optional, Any

import os
from configparser import ConfigParser
from pathlib import Path


class RedshiftConfig:
    ''' redshift settings manager '''

    SECTION = 'redshift'
    TEMP_DAY = 'temp-day'
    TEMP_NIGHT = 'temp-night'
    TRANSITION = 'transition'
    BRIGHTNESS = 'brightness'
    BRIGHTNESS_DAY = 'brightness-day'
    BRIGHTNESS_NIGHT = 'brightness-night'
    GAMMA = 'gamma'

    __defaults = {
        TEMP_DAY: '5000',
        TEMP_NIGHT: '5000',
        TRANSITION: '1',
        BRIGHTNESS: '1',
        BRIGHTNESS_DAY: '1',
        BRIGHTNESS_NIGHT: '1',
        GAMMA: '1',
    }

    path_config = ".config/redshift.conf"
    config: ConfigParser

    def __get_file(self) -> str:
        return os.path.join(str(Path.home()), self.path_config)

    def load(self) -> None:
        ''' load redshift config file '''
        self.config = ConfigParser()
        self.config.read(self.__get_file())

    def save(self) -> None:
        ''' save redshift config file '''
        with open(self.__get_file(), 'w') as file:
            self.config.write(file, space_around_delimiters=False)

    def set_property(self, key: str, value: str) -> None:
        ''' set config redshift property '''
        if self.SECTION not in self.config.sections():
            self.config[self.SECTION] = {}

        self.config[self.SECTION][key] = value

    def get_property(self, key: str, default_value: Optional[Any] = None) -> str:
        ''' get config redshift property '''
        try:
            return self.config[self.SECTION][key]
        except KeyError:
            return str(default_value) or str(self.__defaults.get(key))
