from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(120), unique=True, nullable=False, index=True)
    contraseña = Column(Text, nullable=False)
    rol = Column(String(20), nullable=False)  # admin, mecanico, usuario
    nombre = Column(String(100), nullable=False)
    imagen = Column(String(200), nullable=True)
