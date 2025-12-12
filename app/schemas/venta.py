from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DetalleVentaBase(BaseModel):
    cantidad: int
    precio_unitario: float
    subtotal: float
    descripcion: Optional[str] = None
    producto_id: Optional[int] = None


class DetalleVentaCreate(DetalleVentaBase):
    pass


class DetalleVentaResponse(DetalleVentaBase):
    id: int
    venta_id: int
    
    class Config:
        from_attributes = True


class VentaBase(BaseModel):
    cliente_id: int
    vendedor_id: int
    trabajo_id: Optional[int] = None


class VentaCreate(VentaBase):
    detalles: List[DetalleVentaCreate]


class VentaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    vendedor_id: Optional[int] = None


class VentaResponse(VentaBase):
    id: int
    fecha: datetime
    total: float
    detalles: List[DetalleVentaResponse] = []
    
    class Config:
        from_attributes = True
