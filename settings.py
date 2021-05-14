''' main app settings '''

from typing import Optional, Any

from PyQt5.QtCore import QSettings


class Settings:
    ''' app settings manager '''

    FILE = "redshift_tray"
    config: QSettings = None

    TEMPERATURE_MIN = 'temperature_min'
    TEMPERATURE_MAX = 'temperature_max'
    WINDOW_POSITION = 'window_position'

    __defaults = {
        TEMPERATURE_MIN: '4500',
        TEMPERATURE_MAX: '6500',
        WINDOW_POSITION: '0',
    }

    def __get_file(self) -> str:
        return self.FILE

    def load(self) -> None:
        ''' load redshift_tray config file '''
        self.config = QSettings(self.__get_file())

    def set_property(self, key: str, value: str) -> None:
        ''' set redshift_tray property '''
        self.config.setValue(key, value)

    def get_property(self, key: str, default_value: Optional[Any] = None) -> str:
        ''' get config property '''
        try:
            def_val = default_value or self.__defaults.get(key)
            return self.config.value(key, def_val)
        except KeyError:
            return str(default_value)
