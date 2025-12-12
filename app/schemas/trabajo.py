from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrabajoBase(BaseModel):
    descripcion: str
    estado: str  # pendiente, en proceso, completado, pagado
    costo: Optional[float] = None
    mecanico_id: int
    cliente_id: int


class TrabajoCreate(TrabajoBase):
    pass


class TrabajoUpdate(BaseModel):
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    costo: Optional[float] = None
    mecanico_id: Optional[int] = None
    cliente_id: Optional[int] = None


class TrabajoResponse(TrabajoBase):
    id: int
    foto: Optional[str] = None
    fecha_creacion: datetime
    fecha_cancelacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
