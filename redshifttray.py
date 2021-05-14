''' app '''

from typing import Dict, List, Callable
import sys

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, \
    QAction, QMenu, QMessageBox
from PyQt5.Qt import QIcon

from mainwindow import MainWindow
from settings import Settings
from redshift_config import RedshiftConfig
from redshift_process import RedshiftProcess, RedshiftNotInstalledException
from settings_window import SettingsWindow


class RedshiftTray(QApplication):
    ''' main app class '''

    config: Settings
    window_main: MainWindow
    window_settings: SettingsWindow
    tray_icon: QSystemTrayIcon
    redshift_config: RedshiftConfig
    redshift_proc: RedshiftProcess

    def __init__(self, *args: List[str], **kwargs: Dict[str, str]):
        super().__init__(*args, **kwargs)

        self.setQuitOnLastWindowClosed(False)

        self.__load_config()
        self.__create_windows(self.config, self.redshift_config,
                              self.__update_event, self.__update_settings_event)
        self.__create_tray(self.window_main)
        self.__create_tray_menu(
            self.tray_icon, self.window_main, self.window_settings)
        self.__start_redshift(self.redshift_config)

    def __start_redshift(self, redshift_config: RedshiftConfig) -> None:
        try:
            self.redshift_proc = RedshiftProcess(redshift_config)
            self.redshift_proc.apply()
        except RedshiftNotInstalledException:
            print('Redshift Not Installed')
            QMessageBox(
                QMessageBox.Critical,
                "Redshift Not Installed.",
                "Please install Redshift application first.",
                QMessageBox.Ok
            ).exec()
            sys.exit()

    def __create_tray_menu(self, tray_icon: QSystemTrayIcon,
                           window_main: MainWindow, window_settings: SettingsWindow) -> None:
        show_action = QAction("Show", self)
        settings_action = QAction("Settings", self)
        quit_action = QAction("Exit", self)

        show_action.triggered.connect(window_main.show)
        settings_action.triggered.connect(window_settings.show)
        quit_action.triggered.connect(self.__quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(settings_action)
        tray_menu.addAction(quit_action)

        tray_icon.setContextMenu(tray_menu)

    def __create_windows(self, config: Settings, redshift_config: RedshiftConfig,
                         update_event: Callable, update_settings_event: Callable) -> None:
        self.window_main = MainWindow(
            self, config, redshift_config, update_event)
        self.window_settings = SettingsWindow(config, update_settings_event)

    def __create_tray(self, window_main: MainWindow) -> None:
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("redshift"))
        self.tray_icon.activated.connect(window_main.show)
        self.tray_icon.show()

    def __load_config(self) -> None:
        self.config = Settings()
        self.config.load()

        self.redshift_config = RedshiftConfig()
        self.redshift_config.load()

    def __update_event(self, redshift_new_config: Dict[str, str]) -> None:
        ''' Update UI event. Save and apply new redshift config '''
        self.redshift_config.set_property(
            RedshiftConfig.TEMP_DAY,
            str(redshift_new_config.get(RedshiftConfig.TEMP_DAY))
        )
        self.redshift_config.set_property(
            RedshiftConfig.TEMP_NIGHT,
            str(redshift_new_config.get(RedshiftConfig.TEMP_DAY))
        )
        self.redshift_config.set_property(
            RedshiftConfig.BRIGHTNESS,
            str(redshift_new_config.get(RedshiftConfig.BRIGHTNESS))
        )
        self.redshift_config.set_property(
            RedshiftConfig.BRIGHTNESS_DAY,
            str(redshift_new_config.get(RedshiftConfig.BRIGHTNESS))
        )
        self.redshift_config.set_property(
            RedshiftConfig.BRIGHTNESS_NIGHT,
            str(redshift_new_config.get(RedshiftConfig.BRIGHTNESS))
        )
        self.redshift_config.set_property(
            RedshiftConfig.TRANSITION,
            '0'
        )

        self.redshift_config.save()
        self.redshift_proc.apply()

    def __update_settings_event(self, settings_new_config: Dict[str, str]) -> None:
        ''' Update settings window UI event. Save redshift_tray config and adjust main window UI '''
        self.config.set_property(
            Settings.TEMPERATURE_MIN,
            str(settings_new_config.get(Settings.TEMPERATURE_MIN))
        )
        self.config.set_property(
            Settings.TEMPERATURE_MAX,
            str(settings_new_config.get(Settings.TEMPERATURE_MAX))
        )
        self.config.set_property(
            Settings.WINDOW_POSITION,
            str(settings_new_config.get(Settings.WINDOW_POSITION))
        )

        self.__clamp_temperature()

    def __clamp_temperature(self) -> None:
        ''' Clamp temperature value to max and min limits '''
        temp = self.redshift_config.get_property(RedshiftConfig.TEMP_DAY)
        temp_min = self.config.get_property(Settings.TEMPERATURE_MIN)
        temp_max = self.config.get_property(Settings.TEMPERATURE_MAX)

        temp_clamp = max(temp_min, min(temp, temp_max))

        if temp != temp_clamp:
            self.redshift_config.set_property(
                RedshiftConfig.TEMP_DAY, temp_clamp)
            self.redshift_config.set_property(
                RedshiftConfig.TEMP_NIGHT, temp_clamp)
            self.redshift_config.save()
            self.redshift_proc.apply()

    def __quit(self) -> None:
        ''' Reset redshift to default and quit app'''
        self.redshift_proc.reset()
        QApplication.quit()
