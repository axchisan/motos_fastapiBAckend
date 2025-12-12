from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Usuario:
    """Obtener usuario actual desde el token"""
    payload = decode_access_token(token)
    user_id: int = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales"
        )
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user


def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Verificar que el usuario esté activo"""
    return current_user


def require_role(allowed_roles: list):
    """Decorator para verificar roles de usuario"""
    def role_checker(current_user: Usuario = Depends(get_current_active_user)):
        if current_user.rol not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permisos. Se requiere rol: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


# Shortcuts para roles específicos
def get_admin_user(current_user: Usuario = Depends(require_role(["admin"]))):
    return current_user


def get_mecanico_user(current_user: Usuario = Depends(require_role(["mecanico"]))):
    return current_user


def get_cliente_user(current_user: Usuario = Depends(require_role(["usuario"]))):
    return current_user
