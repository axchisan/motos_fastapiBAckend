from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.deps import get_admin_user, get_mecanico_user, get_cliente_user, get_current_active_user
from app.models.trabajo import Trabajo
from app.models.usuario import Usuario
from app.schemas.trabajo import TrabajoResponse, TrabajoCreate, TrabajoUpdate

router = APIRouter()


@router.get("/", response_model=List[TrabajoResponse])
def listar_trabajos(
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Listar trabajos según rol del usuario"""
    query = db.query(Trabajo)
    
    # Filtrar según rol
    if current_user.rol == "mecanico":
        query = query.filter(Trabajo.mecanico_id == current_user.id)
    elif current_user.rol == "usuario":
        query = query.filter(Trabajo.cliente_id == current_user.id)
    # Admin ve todos
    
    # Filtro por estado
    if estado:
        query = query.filter(Trabajo.estado == estado)
    
    trabajos = query.offset(skip).limit(limit).all()
    return trabajos


@router.get("/estadisticas")
def estadisticas_trabajos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Obtener estadísticas de trabajos (solo admin)"""
    total = db.query(Trabajo).count()
    pendientes = db.query(Trabajo).filter(Trabajo.estado == "pendiente").count()
    en_proceso = db.query(Trabajo).filter(Trabajo.estado == "en proceso").count()
    completados = db.query(Trabajo).filter(Trabajo.estado == "completado").count()
    pagados = db.query(Trabajo).filter(Trabajo.estado == "pagado").count()
    
    return {
        "total": total,
        "pendientes": pendientes,
        "en_proceso": en_proceso,
        "completados": completados,
        "pagados": pagados
    }


@router.get("/{trabajo_id}", response_model=TrabajoResponse)
def obtener_trabajo(
    trabajo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener trabajo por ID"""
    trabajo = db.query(Trabajo).filter(Trabajo.id == trabajo_id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajo no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol == "mecanico" and trabajo.mecanico_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
    if current_user.rol == "usuario" and trabajo.cliente_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
    
    return trabajo


@router.post("/", response_model=TrabajoResponse, status_code=status.HTTP_201_CREATED)
def crear_trabajo(
    trabajo_data: TrabajoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Crear nuevo trabajo (admin o mecanico)"""
    if current_user.rol not in ["admin", "mecanico"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
    
    new_trabajo = Trabajo(**trabajo_data.model_dump())
    new_trabajo.fecha_creacion = datetime.utcnow()
    
    db.add(new_trabajo)
    db.commit()
    db.refresh(new_trabajo)
    
    return new_trabajo


@router.put("/{trabajo_id}", response_model=TrabajoResponse)
def actualizar_trabajo(
    trabajo_id: int,
    trabajo_data: TrabajoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualizar trabajo"""
    trabajo = db.query(Trabajo).filter(Trabajo.id == trabajo_id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajo no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol == "mecanico" and trabajo.mecanico_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
    
    # Actualizar campos
    for field, value in trabajo_data.model_dump(exclude_unset=True).items():
        setattr(trabajo, field, value)
    
    # Si se marca como completado, registrar fecha
    if trabajo_data.estado == "completado" and not trabajo.fecha_cancelacion:
        trabajo.fecha_cancelacion = datetime.utcnow()
    
    db.commit()
    db.refresh(trabajo)
    
    return trabajo


@router.patch("/{trabajo_id}/estado", response_model=TrabajoResponse)
def cambiar_estado_trabajo(
    trabajo_id: int,
    nuevo_estado: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Cambiar estado de un trabajo"""
    trabajo = db.query(Trabajo).filter(Trabajo.id == trabajo_id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajo no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol == "mecanico" and trabajo.mecanico_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
    
    trabajo.estado = nuevo_estado
    
    if nuevo_estado == "completado":
        trabajo.fecha_cancelacion = datetime.utcnow()
    
    db.commit()
    db.refresh(trabajo)
    
    return trabajo


@router.delete("/{trabajo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_trabajo(
    trabajo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Eliminar trabajo (solo admin)"""
    trabajo = db.query(Trabajo).filter(Trabajo.id == trabajo_id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajo no encontrado"
        )
    
    db.delete(trabajo)
    db.commit()
    
    return None
