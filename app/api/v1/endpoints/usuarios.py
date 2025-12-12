from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_admin_user
from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse, UsuarioCreate, UsuarioUpdate
from app.utils.files import save_upload_file

router = APIRouter()


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Listar todos los usuarios (solo admin)"""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Obtener usuario por ID (solo admin)"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Crear nuevo usuario (solo admin)"""
    # Verificar si el correo ya existe
    existing = db.query(Usuario).filter(Usuario.correo == usuario_data.correo).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
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


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Actualizar usuario (solo admin)"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar campos
    if usuario_data.nombre is not None:
        usuario.nombre = usuario_data.nombre
    if usuario_data.correo is not None:
        usuario.correo = usuario_data.correo
    if usuario_data.rol is not None:
        usuario.rol = usuario_data.rol
    if usuario_data.contraseña is not None:
        usuario.contraseña = get_password_hash(usuario_data.contraseña)
    
    db.commit()
    db.refresh(usuario)
    
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Eliminar usuario (solo admin)"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    db.delete(usuario)
    db.commit()
    
    return None


@router.get("/rol/{rol}", response_model=List[UsuarioResponse])
def listar_por_rol(
    rol: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Listar usuarios por rol (admin, mecanico, usuario)"""
    usuarios = db.query(Usuario).filter(Usuario.rol == rol).all()
    return usuarios
