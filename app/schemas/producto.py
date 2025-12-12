from pydantic import BaseModel
from typing import Optional


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: Optional[int] = None
    categoria: Optional[str] = None
    destacado: bool = False


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria: Optional[str] = None
    destacado: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: int
    foto: Optional[str] = None
    
    class Config:
        from_attributes = True
