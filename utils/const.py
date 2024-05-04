from enum import Enum


class CaseFieldIdMap(Enum):
    STRING = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    DATE = "datetime"
    ENUM = "enum"


class BaseTranslateMap:
    class Storage(Enum):
        pass

    class Display(Enum):
        pass

    @property
    def doc(self) -> str:
        return ""


class CaseFieldType(BaseTranslateMap):

    @property
    def doc(self) -> str:
        return "病例字段类型"

    class Storage(BaseTranslateMap.Storage):
        STRING = 1
        INT = 2
        FLOAT = 3
        BOOL = 4
        DATE = 5
        ENUM = 6

    class Display(BaseTranslateMap.Display):
        STRING = "字符串"
        INT = "整数"
        FLOAT = "浮点数"
        BOOL = "布尔值"
        DATE = "日期"
        ENUM = "枚举"
