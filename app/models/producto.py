from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from app.core.database import Base


class Producto(Base):
    __tablename__ = "producto"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=True)
    foto = Column(String(200), nullable=True)
    categoria = Column(String(100), nullable=True)
    destacado = Column(Boolean, default=False)
