# coding:utf-8
from PyQt5.QtCore import Qt, QUrl, QEvent, QObject
from PyQt5.QtGui import QDesktopServices, QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame

from qfluentwidgets import (
    ScrollArea,
    PushButton,
    ToolButton,
    FluentIcon,
    isDarkTheme,
    IconWidget,
    ToolTipFilter,
    TitleLabel,
    CaptionLabel,
    StrongBodyLabel,
    BodyLabel,
    toggleTheme,
)
from gui.common.signal_bus import signalBus


class SeparatorWidget(QWidget):
    """Seperator widget"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(6, 16)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(1)
        pen.setCosmetic(True)
        c = QColor(255, 255, 255, 21) if isDarkTheme() else QColor(0, 0, 0, 15)
        pen.setColor(c)
        painter.setPen(pen)

        x = self.width() // 2
        painter.drawLine(x, 0, x, self.height())


class BaseToolBar(QWidget):
    """Tool bar"""

    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self._customButton()
        self._initWidget()

    def _customButton(self):
        pass

    def _initWidget(self):
        self.setFixedHeight(138)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(0)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(0)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.subtitleLabel.setTextColor(QColor(96, 96, 96), QColor(216, 216, 216))


class BaseCard(QWidget):
    """Base card"""

    def __init__(self, title, widget: QWidget, sourcePath, stretch=0, parent=None):
        super().__init__(parent=parent)
        self.widget = widget
        self.stretch = stretch

        self.titleLabel = StrongBodyLabel(title, self)
        self.card = QFrame(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()

        self._initWidget()

    def _initWidget(self):
        self._initLayout()
        self.card.setObjectName("card")

    def _initLayout(self):
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        self.cardLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        self.topLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(12, 12, 12, 12)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.card, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cardLayout.addLayout(self.topLayout, 0)

        self.widget.setParent(self.card)
        self.topLayout.addWidget(self.widget)
        if self.stretch == 0:
            self.topLayout.addStretch(1)

        self.widget.show()

    def eventFilter(self, obj: QObject, e: QEvent):
        return super().eventFilter(obj, e)


class BaseInterface(ScrollArea):
    """Base interface"""

    def __init__(self, title: str, subtitle: str, parent=None):
        """
        Parameters
        ----------
        title: str
            The title of gallery

        subtitle: str
            The subtitle of gallery

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = self.toolBarClass(title, subtitle, self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName("view")

        self.setQss()
    
    def setQss(self):
        color = "dark" if isDarkTheme() else "light"
        with open(f"resource/qss/{color}/base_interface.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    @property
    def toolBarClass(self):
        return BaseToolBar

    def addCard(self, title, widget, sourcePath: str, stretch=0):
        card = BaseCard(title, widget, sourcePath, stretch, self.view)
        self.vBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignTop)
        return card

    def scrollToCard(self, index: int):
        """scroll to card"""
        w = self.vBoxLayout.itemAt(index).widget()
        self.verticalScrollBar().setValue(w.y())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())
