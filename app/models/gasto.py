from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime
from datetime import datetime
from app.core.database import Base


class Gasto(Base):
    __tablename__ = "gastos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion = Column(Text, nullable=False)
    monto = Column(Float, nullable=False)
    categoria = Column(String(50), nullable=False)
    fecha = Column(Date, nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)
