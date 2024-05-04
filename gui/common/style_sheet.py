from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """Style sheet"""

    BASE_INTERFACE = "base_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/resource/qss/{theme.value.lower()}/{self.value}.qss"
