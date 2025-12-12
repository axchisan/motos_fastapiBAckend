from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import HTTPException, status

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar contraseña usando bcrypt directamente (compatible con Flask-Bcrypt)
    """
    # Convertir strings a bytes
    password_bytes = plain_password.encode('utf-8')
    # Truncar a 72 bytes si es necesario (limitación de bcrypt)
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    hashed_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    """
    Hashear contraseña usando bcrypt directamente (compatible con Flask-Bcrypt)
    """
    # Convertir string a bytes
    password_bytes = password.encode('utf-8')
    # Truncar a 72 bytes si es necesario (limitación de bcrypt)
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generar salt y hashear
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Retornar como string (decodificar de bytes a string)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decodificar JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
