from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.core.deps import get_current_user
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, Token, UsuarioResponse

router = APIRouter()


@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registro(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    # Verificar si el correo ya existe
    existing_user = db.query(Usuario).filter(Usuario.correo == usuario_data.correo).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(usuario_data.contraseña)
    new_user = Usuario(
        correo=usuario_data.correo,
        nombre=usuario_data.nombre,
        rol=usuario_data.rol,
        contraseña=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión - Compatible con Swagger UI
    
    - **username**: Correo electrónico del usuario
    - **password**: Contraseña del usuario
    """
    # Buscar usuario por correo (username en OAuth2 es el correo)
    user = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "rol": user.rol},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/login-json", response_model=Token)
def login_json(credentials: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Iniciar sesión con JSON - Para aplicaciones móviles/frontend
    
    - **correo**: Correo electrónico del usuario
    - **contraseña**: Contraseña del usuario
    """
    # Buscar usuario
    user = db.query(Usuario).filter(Usuario.correo == credentials.correo).first()
    
    if not user or not verify_password(credentials.contraseña, user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "rol": user.rol},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return current_user
