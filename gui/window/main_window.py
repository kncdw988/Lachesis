from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QStackedWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import NavigationInterface, NavigationItemPosition, isDarkTheme, qrouter
from qfluentwidgets.common.icon import FluentIconBase
from qframelesswindow import FramelessWindow

from gui.components.title_bar import CustomTitleBar
from gui.interface.source_interface import SourceInterface


class Widget(QFrame):

    def __init__(self, text: str, parent=None) -> None:
        super().__init__(parent=parent)
        self.setObjectName(text.replace(" ", "-"))
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)

        # leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)


class MainWindow(FramelessWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True, showReturnButton=True)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.sourceInterface = SourceInterface(self)
        self.statisticsInterface = Widget("Statistics Interface", self)
        self.settingInterface = Widget("Setting Interface", self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self) -> None:
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)

    def initNavigation(self) -> None:
        # enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

        self.addSubInterface(self.sourceInterface, FIF.DOCUMENT, "Source Data")

        self.navigationInterface.addSeparator()

        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            "Settings",
            NavigationItemPosition.BOTTOM,
        )

        #!IMPORTANT: don't forget to set the default route key
        qrouter.setDefaultRouteKey(self.stackWidget, self.sourceInterface.objectName())

        # set the maximum width
        # self.navigationInterface.setExpandWidth(300)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(1)

    def initWindow(self) -> None:
        self.resize(900, 700)
        self.setWindowIcon(QIcon("resource/images/logo.png"))
        self.setWindowTitle("Artemis")
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def addSubInterface(
        self,
        interface: Widget,
        icon: FluentIconBase,
        text: str,
        position=NavigationItemPosition.TOP,
    ):
        """add sub interface"""
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
        )

    def setQss(self):
        color = "dark" if isDarkTheme() else "light"
        with open(f"resource/qss/{color}/demo.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())
