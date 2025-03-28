from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime, Enum
from datetime import datetime
from .database import metadata, engine

from enum import Enum as PyEnum

class AlertType(PyEnum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

alerts = Table(
    "alerts",
    metadata,
    Column("id_alerta", Integer, primary_key=True, autoincrement=True),
    Column("datetime", DateTime, nullable=False),
    Column("value", Float, nullable=False),
    Column("version", Integer, nullable=False),
    Column("type", Enum(AlertType), nullable=False),
    Column("sended", Boolean, default=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)

metadata.create_all(engine)
