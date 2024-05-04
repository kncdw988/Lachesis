from service.dao.models import CaseFieldMap
from service.dao.base_dao import BaseDao
from utils import const
from typing import List, Optional
import json
from sqlite3 import IntegrityError
import logging


class CaseFieldMapDao(BaseDao):

    def create(
        self, field_name: str, field_type: const.CaseFieldType.Storage, enum_options: Optional[List[str]] = None
    ) -> CaseFieldMap:
        field_num = self.get_field_num(field_name, field_type)
        try:
            if enum_options:
                self.session.add(
                    CaseFieldMap(
                        field_name=field_name,
                        field_type=field_type.value,
                        enum_options=json.dumps(enum_options),
                        field_num=field_num,
                    )
                )
            else:
                self.session.add(
                    CaseFieldMap(
                        field_name=field_name,
                        field_type=field_type.value,
                        field_num=field_num,
                    )
                )
            self.session.commit()
        except IntegrityError as e:
            logging.warning(f"字段名称重复：{field_name}")
            self.session.close()
        except Exception as e:
            logging.error(f"创建字段映射失败：{e}")
            self.session.close()
        finally:
            db_revc = self.session.get(CaseFieldMap, field_name)
            return db_revc

    def update(self, case_field: CaseFieldMap, field_name: Optional[str] = None, enum_options: Optional[List[str]] = None) -> CaseFieldMap:
        if field_name:
            case_field.field_name = field_name
        if enum_options:
            case_field.enum_options = json.dumps(enum_options)
        self.session.commit()
        return case_field

    def delete(self, field_name: str) -> bool:
        case_field_map = self.session.get(CaseFieldMap, field_name)
        if case_field_map:
            self.session.delete(case_field_map)
            self.session.commit()
            return True
        return False

    def get_by_field_name(self, field_name: str) -> Optional[CaseFieldMap]:
        return self.session.get(CaseFieldMap, field_name)

    def get_field_num(self, field_name: str, field_type: const.CaseFieldType.Storage) -> int:
        last_record = (
            self.session.query(CaseFieldMap)
            .filter(CaseFieldMap.field_type == field_type.value)
            .order_by(CaseFieldMap.field_num.desc())
            .first()
        )
        if last_record:
            return last_record.field_num + 1
        else:
            return 1

    def get_field_id(self, field_name: str, field_type: const.CaseFieldType.Storage) -> str:
        field_num = self.get_field_num(field_name, field_type)
        field_type_id = const.CaseFieldIdMap(field_type.name).value
        return f"field_{field_type_id}_{field_num}"

    def get_case_field_map(self, skip: int = 0, limit: int = 1000) -> List[CaseFieldMap]:
        return self.session.query(CaseFieldMap).all()
