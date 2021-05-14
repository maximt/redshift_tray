''' settings window '''

from typing import Callable, Optional

import os

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.Qt import QIcon
from PyQt5.QtCore import QEvent
from settings import Settings


class SettingsWindow(QDialog):
    ''' settings window '''

    UI_FILE = "views/settings.ui"

    config: Settings
    update_callback: Optional[Callable] = None

    def __init__(self, config: Settings, update_event: Callable):
        super().__init__()
        self.config = config
        self.update_callback = update_event
        self.__load_ui()

    def __load_ui(self) -> None:
        uic.loadUi(os.path.join(os.path.dirname(__file__), self.UI_FILE), self)
        self.setWindowIcon(QIcon.fromTheme("redshift"))
        self.buttonOkCancel.accepted.connect(self.__update_event)

    def __update_ui(self) -> None:
        self.spinTempMin.setValue(
            int(self.config.get_property(Settings.TEMPERATURE_MIN))
        )
        self.spinTempMax.setValue(
            int(self.config.get_property(Settings.TEMPERATURE_MAX))
        )
        self.cmbWindowPos.setCurrentIndex(
            int(self.config.get_property(Settings.WINDOW_POSITION))
        )

    def __update_event(self) -> None:
        cfg = {
            Settings.TEMPERATURE_MIN: self.spinTempMin.value(),
            Settings.TEMPERATURE_MAX: self.spinTempMax.value(),
            Settings.WINDOW_POSITION: self.cmbWindowPos.currentIndex()
        }

        if self.update_callback:
            self.update_callback(cfg)

    def closeEvent(self, event: QEvent) -> None:  # pylint: disable-msg=C0103, C0116
        event.ignore()
        self.hide()

    def showEvent(self, event: QEvent) -> None:  # pylint: disable-msg=C0103, C0116, W0613
        self.__update_ui()
