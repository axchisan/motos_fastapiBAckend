from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

from app.core.database import get_db
from app.core.deps import get_admin_user
from app.models.gasto import Gasto
from app.models.usuario import Usuario
from app.schemas.gasto import GastoResponse, GastoCreate, GastoUpdate

router = APIRouter()


@router.get("/", response_model=List[GastoResponse])
def listar_gastos(
    skip: int = 0,
    limit: int = 100,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Listar gastos con filtros (solo admin)"""
    # Filtro base: solo hoy por defecto
    if not fecha_inicio and not fecha_fin:
        hoy = date.today()
        fecha_inicio = hoy
        fecha_fin = hoy
    
    query = db.query(Gasto)
    
    # Filtro por fechas
    if fecha_inicio:
        query = query.filter(Gasto.fecha >= fecha_inicio)
    
    if fecha_fin:
        query = query.filter(Gasto.fecha <= fecha_fin)
    
    # Filtro por categoría
    if categoria:
        query = query.filter(Gasto.categoria == categoria)
    
    gastos = query.order_by(Gasto.fecha.desc()).offset(skip).limit(limit).all()
    return gastos


@router.get("/total")
def total_gastos(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Obtener total de gastos por período"""
    if not fecha_inicio and not fecha_fin:
        hoy = date.today()
        fecha_inicio = hoy
        fecha_fin = hoy
    
    query = db.query(Gasto)
    
    if fecha_inicio:
        query = query.filter(Gasto.fecha >= fecha_inicio)
    
    if fecha_fin:
        query = query.filter(Gasto.fecha <= fecha_fin)
    
    gastos = query.all()
    total = sum(gasto.monto for gasto in gastos)
    
    return {
        "cantidad_gastos": len(gastos),
        "total": total,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }


@router.get("/categorias", response_model=List[str])
def listar_categorias(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Obtener lista de categorías únicas"""
    categorias = db.query(Gasto.categoria).distinct().all()
    return [c[0] for c in categorias if c[0]]


@router.get("/{gasto_id}", response_model=GastoResponse)
def obtener_gasto(
    gasto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Obtener gasto por ID"""
    gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto no encontrado"
        )
    return gasto


@router.post("/", response_model=GastoResponse, status_code=status.HTTP_201_CREATED)
def crear_gasto(
    gasto_data: GastoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Crear nuevo gasto (solo admin)"""
    nuevo_gasto = Gasto(**gasto_data.model_dump())
    
    db.add(nuevo_gasto)
    db.commit()
    db.refresh(nuevo_gasto)
    
    return nuevo_gasto


@router.put("/{gasto_id}", response_model=GastoResponse)
def actualizar_gasto(
    gasto_id: int,
    gasto_data: GastoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Actualizar gasto (solo admin)"""
    gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto no encontrado"
        )
    
    # Actualizar campos
    for field, value in gasto_data.model_dump(exclude_unset=True).items():
        setattr(gasto, field, value)
    
    db.commit()
    db.refresh(gasto)
    
    return gasto


@router.delete("/{gasto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_gasto(
    gasto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Eliminar gasto (solo admin)"""
    gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto no encontrado"
        )
    
    db.delete(gasto)
    db.commit()
    
    return None
