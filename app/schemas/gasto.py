from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class GastoBase(BaseModel):
    descripcion: str
    monto: float
    categoria: str
    fecha: date


class GastoCreate(GastoBase):
    pass


class GastoUpdate(BaseModel):
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    categoria: Optional[str] = None
    fecha: Optional[date] = None


class GastoResponse(GastoBase):
    id: int
    creado_en: datetime
    
    class Config:
        from_attributes = True
