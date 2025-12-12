from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    correo: EmailStr
    nombre: str
    rol: str


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol: Optional[str] = None
    contraseña: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id: int
    imagen: Optional[str] = None
    
    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    correo: EmailStr
    contraseña: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UsuarioResponse
