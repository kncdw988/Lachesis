from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import JSON, Integer, DateTime, Float
from sqlalchemy import create_engine
from utils import config

engine = create_engine(config.SQLITE_DATABASE_URI, echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    name: Mapped[str]
    client_id: Mapped[str]


class PatientCase(Base):

    __tablename__ = "patient_case"

    id: Mapped[str] = mapped_column(primary_key=True)
    admission_number: Mapped[str]
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    create_by: Mapped[str]
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    update_by: Mapped[str]
    field_int_1: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_2: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_3: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_4: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_5: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_6: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_7: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_8: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_9: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_10: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_11: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_12: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_13: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_14: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_15: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_16: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_17: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_18: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_19: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_20: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_21: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_22: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_23: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_24: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_25: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_26: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_27: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_28: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_29: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    field_int_30: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    field_float_1: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_3: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_4: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_5: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_6: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_7: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_8: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_9: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_10: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_11: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_12: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_13: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_14: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_15: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_16: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_17: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_18: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_19: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_20: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_21: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_22: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_23: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_24: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_25: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_26: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_27: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_28: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_29: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_float_30: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    field_str_1: Mapped[Optional[str]]
    field_str_2: Mapped[Optional[str]]
    field_str_3: Mapped[Optional[str]]
    field_str_4: Mapped[Optional[str]]
    field_str_5: Mapped[Optional[str]]
    field_str_6: Mapped[Optional[str]]
    field_str_7: Mapped[Optional[str]]
    field_str_8: Mapped[Optional[str]]
    field_str_9: Mapped[Optional[str]]
    field_str_10: Mapped[Optional[str]]
    field_str_11: Mapped[Optional[str]]
    field_str_12: Mapped[Optional[str]]
    field_str_13: Mapped[Optional[str]]
    field_str_14: Mapped[Optional[str]]
    field_str_15: Mapped[Optional[str]]
    field_str_16: Mapped[Optional[str]]
    field_str_17: Mapped[Optional[str]]
    field_str_18: Mapped[Optional[str]]
    field_str_19: Mapped[Optional[str]]
    field_str_20: Mapped[Optional[str]]
    field_str_21: Mapped[Optional[str]]
    field_str_22: Mapped[Optional[str]]
    field_str_23: Mapped[Optional[str]]
    field_str_24: Mapped[Optional[str]]
    field_str_25: Mapped[Optional[str]]
    field_str_26: Mapped[Optional[str]]
    field_str_27: Mapped[Optional[str]]
    field_str_28: Mapped[Optional[str]]
    field_str_29: Mapped[Optional[str]]
    field_str_30: Mapped[Optional[str]]

    field_datetime_1: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_2: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_3: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_4: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_5: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_6: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_7: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_8: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_9: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    field_datetime_10: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    field_enum_1: Mapped[Optional[str]]
    field_enum_2: Mapped[Optional[str]]
    field_enum_3: Mapped[Optional[str]]
    field_enum_4: Mapped[Optional[str]]
    field_enum_5: Mapped[Optional[str]]
    field_enum_6: Mapped[Optional[str]]
    field_enum_7: Mapped[Optional[str]]
    field_enum_8: Mapped[Optional[str]]
    field_enum_9: Mapped[Optional[str]]
    field_enum_10: Mapped[Optional[str]]
    field_enum_11: Mapped[Optional[str]]
    field_enum_12: Mapped[Optional[str]]
    field_enum_13: Mapped[Optional[str]]
    field_enum_14: Mapped[Optional[str]]
    field_enum_15: Mapped[Optional[str]]
    field_enum_16: Mapped[Optional[str]]
    field_enum_17: Mapped[Optional[str]]
    field_enum_18: Mapped[Optional[str]]
    field_enum_19: Mapped[Optional[str]]
    field_enum_20: Mapped[Optional[str]]


class CaseFieldMap(Base):

    __tablename__ = "case_field_map"

    field_name: Mapped[str] = mapped_column(primary_key=True)
    field_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enum_options: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    field_num: Mapped[int]
