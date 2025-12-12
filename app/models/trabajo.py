from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Trabajo(Base):
    __tablename__ = "trabajo"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    estado = Column(String(50), nullable=False)  # pendiente, en proceso, completado, pagado
    foto = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    costo = Column(Float, nullable=True)
    fecha_cancelacion = Column(DateTime, nullable=True)
    
    mecanico_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
