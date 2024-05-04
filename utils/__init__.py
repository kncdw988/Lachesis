from utils import const
import sys


class Translater:

    def __init__(self, map: const.BaseTranslateMap):
        self.map = map

    def display_to_storage(self, display: const.BaseTranslateMap.Display) -> const.BaseTranslateMap.Storage:
        if hasattr(self.map.Storage, display.name):
            return getattr(self.map.Storage, display.name)
        raise ValueError(f"{display.name}不是一个有效的{self.map.doc}")

    def storage_to_display(self, storage: const.BaseTranslateMap.Storage) -> const.BaseTranslateMap.Display:
        if hasattr(self.map.Display, storage.name):
            return getattr(self.map.Display, storage.name)
        raise ValueError(f"{storage.name}不是一个有效的{self.map.doc}")

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000
