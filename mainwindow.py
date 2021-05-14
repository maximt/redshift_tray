''' main app window '''

from typing import Callable, Optional

import os
from PyQt5 import uic
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QIcon

from display_utils import DisplayUtils, WindowPos
from redshift_config import RedshiftConfig
from settings import Settings


class MainWindow(QWidget):
    ''' main window '''

    UI_FILE = "views/mainwindow.ui"
    app: 'RedshiftTray'
    config: Settings
    redshift_config: RedshiftConfig
    update_callback: Optional[Callable] = None
    grp_temp_title: str = 'Color temperature'
    grp_brightness_title: str = 'Brightness'

    def __init__(self, app: 'RedshiftTray',
                 config: Settings,
                 redshift_config: RedshiftConfig,
                 update_callback: Callable):
        super().__init__()
        self.app = app
        self.config = config
        self.redshift_config = redshift_config
        self.update_callback = update_callback
        self.__load_ui()

    def __load_ui(self) -> None:
        uic.loadUi(os.path.join(os.path.dirname(__file__), self.UI_FILE), self)
        self.setWindowIcon(QIcon.fromTheme("redshift"))
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint | Qt.Popup)

        self.sliderBrightness.valueChanged.connect(self.__update_ui)
        self.sliderTemp.valueChanged.connect(self.__update_ui)

        self.btnApply.clicked.connect(self.__update_event)

        self.grp_temp_title = self.grpTemp.title()
        self.grp_brightness_title = self.grpBrightness.title()

        self.__update_ui()

        self.setWindowModality(Qt.ApplicationModal)
        self.setFocus()

    def __update_ui(self) -> None:
        temp = str(self.sliderTemp.value())
        brightness = str(float(self.sliderBrightness.value()) / 100.0)

        self.lblTemp.setText(temp)
        self.lblBrightness.setText(brightness)

        self.grpTemp.setTitle(
            "{} ({})".format(
                self.grp_temp_title,
                self.redshift_config.get_property(RedshiftConfig.TEMP_DAY)
            )
        )
        self.grpBrightness.setTitle(
            "{} ({})".format(
                self.grp_brightness_title,
                self.redshift_config.get_property(RedshiftConfig.BRIGHTNESS)
            )
        )

    def __update_event(self) -> None:
        brightness = float(self.sliderBrightness.value()) / 100.0
        temp = int(self.sliderTemp.value())

        cfg = {
            RedshiftConfig.BRIGHTNESS: brightness,
            RedshiftConfig.TEMP_DAY: temp,
        }

        if self.update_callback:
            self.update_callback(cfg)
        self.__update_ui()

    def closeEvent(self, event: QEvent) -> None:  # pylint: disable-msg=C0103, C0116
        event.ignore()
        self.hide()

    def changeEvent(self, event: QEvent) -> None:  # pylint: disable-msg=C0103, C0116
        if event.type() == QEvent.ActivationChange \
                and not self.isActiveWindow():
            self.hide()

    def showEvent(self, event: QEvent) -> None:  # pylint: disable-msg=C0103, C0116, W0613
        self.__load_config()
        self.__update_ui()

        window_pos = WindowPos(
            int(self.config.get_property(Settings.WINDOW_POSITION, 0)))
        pos = DisplayUtils.get_window_pos(self, window_pos)
        self.move(pos)

    def __load_config(self) -> None:
        brightness = int(float(self.redshift_config.get_property(
            RedshiftConfig.BRIGHTNESS)) * 100)
        self.sliderBrightness.setValue(brightness)

        mintmp = int(self.config.get_property(Settings.TEMPERATURE_MIN))
        maxtmp = int(self.config.get_property(Settings.TEMPERATURE_MAX))
        tmp = int(self.redshift_config.get_property(RedshiftConfig.TEMP_DAY))

        tmp = max(mintmp, min(tmp, maxtmp))  # clamp to range

        self.sliderTemp.setMinimum(mintmp)
        self.sliderTemp.setMaximum(maxtmp)
        self.sliderTemp.setValue(tmp)
