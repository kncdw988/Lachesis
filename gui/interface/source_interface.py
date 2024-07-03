from gui.interface import BaseInterface, BaseToolBar
from qfluentwidgets import (
    CardWidget,
    TableWidget,
    ToolButton,
    FluentIcon,
    ToolTipFilter,
    MSFluentTitleBar,
    isDarkTheme,
    TransparentToolButton,
    RoundMenu,
    Action,
    StrongBodyLabel, PushButton, LineEdit, PlainTextEdit,
    MessageBoxBase, ComboBox, InfoBar, InfoBarPosition, PrimaryPushButton,
    FlowLayout
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QButtonGroup
from utils import isWin11
from qframelesswindow import AcrylicWindow as Window
from service.case_field_config import CaseFieldConfigService
from utils import const
from functools import partial
from typing import Optional, Dict


class FieldConfigBox(MessageBoxBase):

    def __init__(self, parent=None, field_name: Optional[str] = None, field_type: Optional[str] = None, is_edit: bool = False):
        super().__init__(parent)
        self.field_name = field_name if field_name else ""
        self.field_type = field_type if field_type else ""
        self.old_field_name = field_name if field_name else ""
        self.enum_options = ""
        self.is_edit = is_edit

        self.input_card()

        self.yesButton.setText("保存")
        self.yesButton.setDisabled(True)
        self.yesButton.clicked.connect(self.save)
        self.cancelButton.setText("取消")
        self.widget.setMinimumWidth(400)
        self.widget.setMinimumHeight(400)


    def input_card(self):
        card = QWidget(self)
        field_name_label = StrongBodyLabel("字段名称")
        field_name_input = LineEdit()
        field_name_input.setPlaceholderText("请输入字段名称")
        if self.field_name:
            field_name_input.setText(self.field_name)
        field_name_input.setFixedWidth(300)
        field_name_input.setClearButtonEnabled(True)
        field_name_input.textChanged.connect(self._validate_field_name_input)

        field_type_label = StrongBodyLabel("字段类型")
        field_type_input = ComboBox()
        field_type_input.setPlaceholderText("请选择")
        items = [i.value for i in const.CaseFieldType.Display]
        field_type_input.addItems(items)
        if self.field_type:
            field_type_input.setCurrentIndex(items.index(self.field_type))
        else:
            field_type_input.setCurrentIndex(-1)
        field_type_input.setStyleSheet("QComboBox::drop-down {background:white}")
        field_type_input.setStyleSheet("QComboBox::drop-down {background:white}")
        field_type_input.setFixedWidth(300)
        # field_type_input.currentIndexChanged.connect(self._validate_field_type_input)
        field_type_input.currentTextChanged.connect(self._validate_field_type_input)

        enum_options_label = StrongBodyLabel("选项")
        enum_options_input = PlainTextEdit()
        enum_options_input.setPlaceholderText("请输入选项，多个选项用逗号分隔")
        if self.field_type in [const.CaseFieldType.Display.ENUM.value]:
            enum_options = CaseFieldConfigService().get(field_name=self.field_name).enum_options
            if enum_options:
                enum_options_input.setPlainText(enum_options[1:-1])
        enum_options_input.setFixedWidth(300)
        enum_options_input.setFixedHeight(100)
        enum_options_input.textChanged.connect(partial(self._validate_enum_options_input, enum_options_input))

        layout = QVBoxLayout(self)
        layout.addWidget(field_name_label, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(field_name_input, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(field_type_label, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(field_type_input, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(enum_options_label, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(enum_options_input, 0, Qt.AlignmentFlag.AlignCenter)
        card.setLayout(layout)
        self.viewLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignCenter)

    def _enable_yes_button(self):
        if self.field_name:
            if self.field_type:
                if self.field_type not in [const.CaseFieldType.Display.ENUM.value]:
                    self.yesButton.setDisabled(False)
                    return
                else:
                    if self.enum_options:
                        self.yesButton.setDisabled(False)
                        return
        self.yesButton.setDisabled(True)
        return

    def _validate_field_name_input(self, text):
        self.field_name = text
        self._enable_yes_button()

    def _validate_field_type_input(self, text):
        self.field_type = text
        self._enable_yes_button()

    def _validate_enum_options_input(self, input: PlainTextEdit, **kwargs):
        self.enum_options = input.toPlainText()
        self._enable_yes_button()

    def save(self):
        try:
            field_service = CaseFieldConfigService()
            if not self.is_edit:
                if self.enum_options:
                    enum_options = self.enum_options.replace("，", ",")
                    new_field_config = field_service.add_new_field_config(
                        field_name=self.field_name, field_type_display=self.field_type, enum_options=enum_options.split(",")
                    )
                else:
                    new_field_config = field_service.add_new_field_config(
                        field_name=self.field_name, field_type_display=self.field_type
                    )
                if new_field_config:
                    self.parent().add_card(self.field_name, self.field_type)
            else:
                if self.enum_options:
                    enum_options = self.enum_options.replace("，", ",")
                    res = field_service.update_field_config(
                        old_field_name=self.old_field_name, field_name=self.field_name if self.field_name else None, enum_options=enum_options.split(",") if self.enum_options else None
                    )
                else:
                    res = field_service.update_field_config(
                        old_field_name=self.old_field_name, field_name=self.field_name if self.field_name else None
                    )
                if res:
                    self.parent().update_card(self.old_field_name, self.field_name)
        except Exception as e:
            self.parent().error_info_bar(str(e))


class MicaWindow(Window):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(MSFluentTitleBar(self))
        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())


class FieldConfigCard(CardWidget):

    def __init__(self, field_name: str, field_type: str, parent=None):
        super().__init__(parent=parent)

        self.field_name = field_name
        self.field_type = field_type
        self.fieldConfigWidget = QWidget(self)
        self.fieldNameLabel = StrongBodyLabel(field_name[:15])
        if  len(field_name) > 15:
            self.fieldNameLabel.setToolTip(field_name)
        self.fieldTypeLabel = StrongBodyLabel(field_type)
        self.fieldNameLabel.setFixedWidth(250)
        self.fieldTypeLabel.setFixedWidth(50)
        self.moreButton = TransparentToolButton(FluentIcon.MORE)
        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)
        self.fieldConfigLayout = QHBoxLayout()
        self.fieldConfigLayout.addWidget(self.fieldNameLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.fieldConfigLayout.addWidget(self.fieldTypeLabel, 0, Qt.AlignmentFlag.AlignRight)
        self.fieldConfigLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)
        self.fieldConfigLayout.setSpacing(1)
        self.fieldConfigWidget.setLayout(self.fieldConfigLayout)
        
        self.vBoxLayout = QVBoxLayout(self)


        self.vBoxLayout.addWidget(self.fieldConfigWidget, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        update_action = Action(FluentIcon.EDIT, "编辑", self)
        update_action.triggered.connect(self.update_card)
        delete_action = Action(FluentIcon.DELETE, "删除", self)
        delete_action.triggered.connect(self.delete_card)
        menu.addAction(update_action)
        menu.addAction(delete_action)

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)

    def delete_card(self):
        if CaseFieldConfigService().delete_field_config(self.field_name):
            self.hide()
            del self.parent()._card_map[self.field_name]

    def update_card(self):
        w = FieldConfigBox(self.parent(), field_name=self.field_name, field_type=self.field_type, is_edit=True)
        w.exec()

class ConfigFieldWindow(MicaWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = CaseFieldConfigService()
        self._table = self.service.table
        self._card_map: Dict[str, FieldConfigCard] = {}

        self.resize(600, 500)
        self.add_field = PushButton(FluentIcon.ADD, "新增", self)
        self.add_field.clicked.connect(self.add_row)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 60, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.add_field, 0, Qt.AlignmentFlag.AlignLeft)
        self.initCard()

    def initCard(self):
        for item in self._table:
            card = FieldConfigCard(item[0], item[1], self)
            self._card_map[item[0]] = card
            self.vBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignTop)

    def refresh_card(self, field_name: str, field_type: str):
        card = self._card_map.get(field_name)
        if card:
            card.field_name = field_name
            card.field_type = field_type
            card.fieldNameLabel.setText(field_name[:15])
            if len(field_name) > 15:
                card.fieldNameLabel.setToolTip(field_name)
            card.fieldTypeLabel.setText(field_type)
            card.update()
        else:
            card = FieldConfigCard(field_name, field_type, self)
            self._card_map[field_name] = card
            self.vBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignTop)

    def add_card(self, field_name: str, field_type: str):
        card = FieldConfigCard(field_name, field_type, self)
        self._card_map[field_name] = card
        self.vBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignTop)
    
    def update_card(self, old_field_name: str, field_name: str):
        card = self._card_map.get(old_field_name)
        if card:
            card.field_name = field_name
            card.fieldNameLabel.setText(field_name[:15])
            if len(field_name) > 15:
                card.fieldNameLabel.setToolTip(field_name)
            card.update()
            self._card_map[field_name] = card
            del self._card_map[old_field_name]


    def add_row(self):
        w = FieldConfigBox(self)
        w.exec()

    def error_info_bar(self, error_message: str):
        w = InfoBar.error(
            title='Error',
            content=error_message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self
        )
        w.show()


class AddCaseWindow(MicaWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = CaseFieldConfigService()
        self._table = self.service.table

        self.button_group = QWidget(self)
        self.button_group_layout = QHBoxLayout()
        yesButton = PrimaryPushButton(FluentIcon.SAVE, "保存")
        cancelButton = PushButton(FluentIcon.CANCEL, "取消")
        self.button_group_layout.addWidget(cancelButton, 0, Qt.AlignmentFlag.AlignJustify)
        self.button_group_layout.addWidget(yesButton, 0, Qt.AlignmentFlag.AlignJustify)
        self.button_group.setLayout(self.button_group_layout)

        view_widget = QWidget(self)
        view_widget_laylout = FlowLayout()
        view_widget_laylout.setSpacing(6)
        view_widget_laylout.setContentsMargins(30, 60, 30, 30)
        view_widget_laylout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        view_widget.setLayout(view_widget_laylout)

        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 60, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vBoxLayout.addWidget(view_widget, 0, Qt.AlignmentFlag.AlignJustify)
        self.vBoxLayout.addWidget(self.button_group, 0, Qt.AlignmentFlag.AlignTrailing)

        self.adjustSize()


class SourceToolBar(BaseToolBar):

    def _customButton(self):
        self.configField = ToolButton(FluentIcon.LABEL, self)
        self.addCaseButton = ToolButton(FluentIcon.ADD, self)

    def _initWidget(self):
        super()._initWidget()
        self.buttonLayout.addWidget(self.configField, 0, Qt.AlignmentFlag.AlignRight)
        self.configField.installEventFilter(ToolTipFilter(self.configField))
        self.configField.setToolTip(self.tr("字段配置"))
        self.configField.clicked.connect(self.click_configField)

        self.buttonLayout.addWidget(self.addCaseButton, 0, Qt.AlignmentFlag.AlignRight)
        self.addCaseButton.installEventFilter(ToolTipFilter(self.addCaseButton))
        self.addCaseButton.setToolTip(self.tr("新增数据"))
        self.addCaseButton.clicked.connect(self.click_addCaseButton)

    def click_configField(self):
        w = ConfigFieldWindow()
        w.show()

    def click_addCaseButton(self):
        w = AddCaseWindow()
        w.show()


class SourceInterface(BaseInterface):

    def __init__(self, parent=None):
        super().__init__(title="", subtitle="", parent=parent)
        # table view
        self.addCard(title="", widget=TableWidget(self), sourcePath="")

    @property
    def toolBarClass(self):
        return SourceToolBar
