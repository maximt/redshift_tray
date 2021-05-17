''' display helpers to get window position '''

from enum import Enum

from PyQt5.QtCore import QRect, QPoint
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget


class WindowPos(Enum):
    ''' main window position '''
    C = 0
    TL = 1
    TR = 2
    BR = 3
    BL = 4


class DisplayUtils:
    ''' display resolution helpers '''

    @staticmethod
    def get_used_screen_area() -> QRect:
        ''' Get screen area except panels and dockbars. Qt5 is buggy, use Gtk instead '''
        try:
            import gi
            from gi.repository import Gdk

            gi.require_version('Gtk', '3.0')
            gi.require_version('Gdk', '3.0')

            display = Gdk.Display()
            w_area = display.get_default() \
                .get_primary_monitor() \
                .get_workarea()

            return QRect(w_area.x, w_area.y, w_area.width, w_area.height)
        except Exception:  # pylint: disable-msg=W0703:
            return None

    @staticmethod
    def get_screen_center() -> QPoint:
        ''' Center of current display '''
        return QtWidgets.QDesktopWidget().screenGeometry().center()

    @staticmethod
    def get_window_center(window: QWidget) -> QPoint:
        ''' Center of window '''
        center = DisplayUtils.get_screen_center()
        size = window.size()
        return QPoint(center.x() - size.width() / 2, center.y() - size.height() / 2)

    @staticmethod
    def get_window_pos(window: QWidget, pos: WindowPos) -> QPoint:
        ''' Get window position: Center, TopLeft, TopRight, BottomLeft, BottomRight '''
        center = DisplayUtils.get_window_center(window)
        area = DisplayUtils.get_used_screen_area()

        if not area:
            return center

        if pos == WindowPos.TL:
            center = area.topLeft()
        elif pos == WindowPos.TR:
            center = QPoint(
                area.right() - window.width(),
                area.top()
            )
        elif pos == WindowPos.BR:
            center = QPoint(
                area.right() - window.width(),
                area.bottom() - window.height()
            )
        elif pos == WindowPos.BL:
            center = QPoint(
                area.left(),
                area.bottom() - window.height()
            )
        elif pos == WindowPos.C:
            pass

        return center
