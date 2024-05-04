from qfluentwidgets import ScrollArea, ExpandLayout, SettingCardGroup
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QStyleOptionViewItem,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QUrl, QModelIndex, QSize, pyqtSignal, pyqtBoundSignal
from gui.interface import BaseInterface, BaseToolBar
from qfluentwidgets import (
    TextEdit,
    TableWidget,
    LineEditButton,
    LineEditMenu,
    LineEdit,
    MessageBox,
    Dialog,
    SubtitleLabel,
    MessageBoxBase,
    ComboBox,
    TableItemDelegate,
)
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
from PyQt5.QtGui import QPalette
from service.case_field_config import CaseFieldConfigService
from utils import const
from functools import partial
from typing import List


class FieldTypeComboBox(ComboBox):
    validation_signal = pyqtBoundSignal(str)


class FieldConfigTable(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = CaseFieldConfigService()
        self._table = self.service.table

        # select row on right-click
        self.setSelectRightClickedRow(True)

        self.setBorderVisible(True)
        self.setBorderRadius(8)

        self.setWordWrap(False)
        self.setRowCount(len(self._table))
        self.setColumnCount(4)

        self.verticalHeader().hide()
        self.setHorizontalHeaderLabels(["字段名称", "字段类型", "选项", "操作"])

        self.fill_table()

        self.setColumnWidth(0, 110)
        self.setColumnWidth(1, 110)
        self.setColumnWidth(2, 250)
        self.setColumnWidth(3, 50)
        self.resizeRowsToContents()

    def row_delete_button(self, row_index: int) -> QWidget:
        button = ToolButton(FluentIcon.DELETE, self)
        button.clicked.connect(partial(self.delete_row, row_index))
        layout = QVBoxLayout()
        layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def field_type_widget(self, field_type: str):
        combo_box = FieldTypeComboBox()
        combo_box.setPlaceholderText("请选择")
        items = [i.value for i in const.CaseFieldType.Display]
        combo_box.addItems(items)
        if field_type:
            combo_box.setCurrentIndex(items.index(field_type))
        else:
            combo_box.setCurrentIndex(-1)
        combo_box.validation_signal = pyqtBoundSignal(str)
        combo_box.setStyleSheet("QComboBox::drop-down {background:white}")
        # 设置选中的文字左对齐
        combo_box.adjustSize()
        layout = QHBoxLayout()
        layout.addWidget(combo_box, 0, Qt.AlignmentFlag.AlignHCenter)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def field_name_item(self, field_name: str):
        widget = QTableWidgetItem(field_name)
        widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return widget

    def enum_options_item(self, enum_options: str):
        widge = QTableWidgetItem(enum_options)
        widge.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return widge

    def fill_table(self):
        for r_index, row in enumerate(self._table):

            self.setItem(r_index, 0, self.field_name_item(row[0]))
            self.setCellWidget(r_index, 1, self.field_type_widget(row[1]))
            self.setItem(r_index, 2, self.enum_options_item(row[2]))
            # Add delete button for the row
            self.setCellWidget(r_index, 3, self.row_delete_button(row_index=r_index))

    def delete_row(self, row_index: int):
        self.setRowHidden(row_index, True)
        self.update()

    def add_row(self):
        row_index = self.rowCount()
        self.setRowCount(row_index + 1)
        self.setItem(row_index, 0, self.field_name_item(""))
        self.setCellWidget(row_index, 1, self.field_type_widget(""))
        self.setItem(row_index, 2, self.enum_options_item(""))
        self.setCellWidget(row_index, 3, self.row_delete_button(row_index=row_index))
        self.resizeRowsToContents()
        self.update()

    def get_table(self) -> List[List[str]]:
        table = []
        for row_index in range(self.rowCount()):
            if self.isRowHidden(row_index):
                continue
            field_name = self.item(row_index, 0).text()
            if not field_name:
                continue
            field_type_widget: FieldTypeComboBox = self.cellWidget(row_index, 1).children()[1]
            field_type = field_type_widget.currentText()
            if field_type == "":
                self.show_error_tip(field_type_widget, "请选择字段类型")
                raise ValueError("请选择字段类型")
            enum_options = self.item(row_index, 2).text()
            table.append([field_name, field_type, enum_options])
        return table


class FieldConfigBox(MessageBoxBase):
    """Custom message box"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("字段配置", self)

        self.add_field = ToolButton(FluentIcon.ADD, self)
        self.add_field.installEventFilter(ToolTipFilter(self.add_field))
        self.add_field.setToolTip("添加配置")
        self.add_field.clicked.connect(self.add_row)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.add_field)

        self.table_view = FieldConfigTable(self)

        self.viewLayout.addWidget(self.table_view)

        # change the text of button
        self.yesButton.setText("保存")
        self.yesButton.clicked.connect(self.save)
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(580)
        self.widget.setMinimumHeight(620)

    def add_row(self):
        self.table_view.add_row()

    def save(self):
        try:
            table = self.table_view.get_table()
            print(table)
        except:
            self.update()


class SourceToolBar(BaseToolBar):

    def _customButton(self):
        self.configField = ToolButton(FluentIcon.LABEL, self)

    def _initWidget(self):
        super()._initWidget()
        self.buttonLayout.addWidget(self.configField, 0, Qt.AlignmentFlag.AlignRight)

        self.configField.installEventFilter(ToolTipFilter(self.configField))

        self.configField.setToolTip(self.tr("字段配置"))

        self.configField.clicked.connect(self.click_configField)

    def click_configField(self):
        w = FieldConfigBox(self.parent())
        w.exec()


class SourceInterface(BaseInterface):

    def __init__(self, parent=None):
        super().__init__(title="", subtitle="", parent=parent)
        # self.setObjectName('sourceInterface')

        self.addCard(title="筛选", widget=LineEdit(self), sourcePath="")

        # table view
        self.addCard(title="", widget=TableWidget(self), sourcePath="")

    @property
    def toolBarClass(self):
        return SourceToolBar
