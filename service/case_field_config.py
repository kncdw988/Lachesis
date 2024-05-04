from service.dao.case_field_map import CaseFieldMapDao
from service.dao.models import CaseFieldMap
from utils import const
from typing import List, Dict, Optional
import json
from utils import Translater


class CaseFieldConfigService:

    def __init__(self) -> None:
        self.dao = CaseFieldMapDao()
        self._map = self.get_map()

    @property
    def table(self) -> List[List[str]]:
        table = []
        for _, field_config in self._map.items():
            field_type_storage = const.CaseFieldType.Storage(field_config.field_type)
            field_type_display = const.CaseFieldType.Display[field_type_storage.name]
            if field_type_storage == const.CaseFieldType.Storage.ENUM:
                enum_options = field_config.enum_options[1:-1] if field_config.enum_options else ""
            else:
                enum_options = ""
            row = [field_config.field_name, field_type_display.value, enum_options]
            table.append(row)
        return table

    def get_map(self) -> Dict[str, CaseFieldMap]:
        all_config = self.dao.get_case_field_map()
        field_map = {}
        for field_config in all_config:
            field_map[field_config.field_name] = field_config
        return field_map

    def get_all(self):
        return CaseFieldMapDao().get_case_field_map()

    def get(self, field_name: str) -> Optional[CaseFieldMap]:
        return self._map.get(field_name)

    def add_new_field_config(self, field_name: str, field_type_display: str, enum_options: List[str] = None) -> bool:
        field_type = const.CaseFieldType.Storage[const.CaseFieldType.Display(field_type_display).name]
        db_rv = self.dao.create(field_name=field_name, field_type=field_type, enum_options=enum_options)
        if db_rv:
            self._map[field_name] = db_rv
            return True
        return False

    def update_field_config(self, old_field_name: str, field_name: str=None, enum_options: List[str] = None) -> bool:
        case_field = self.get(old_field_name)
        if case_field:
            case_field = self.dao.update(case_field=case_field, field_name=field_name, enum_options=enum_options)
            del self._map[old_field_name]
            self._map[case_field.field_name] = case_field
            return True
        return False
    
    def delete_field_config(self, field_name: str) -> bool:
        if self.dao.delete(field_name=field_name):
            del self._map[field_name]
            return True
        return False
    
