from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Venta(Base):
    __tablename__ = "venta"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    total = Column(Float, nullable=False, default=0.0)
    
    cliente_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    trabajo_id = Column(Integer, ForeignKey("trabajo.id"), nullable=True)
    
    # Relaciones
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")


class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    descripcion = Column(String(255), nullable=True)
    
    venta_id = Column(Integer, ForeignKey("venta.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=True)
    
    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
