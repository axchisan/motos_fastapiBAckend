from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta

from app.core.database import get_db
from app.core.deps import get_admin_user
from app.models.venta import Venta, DetalleVenta
from app.models.usuario import Usuario
from app.schemas.venta import VentaResponse, VentaCreate, VentaUpdate

router = APIRouter()


@router.get("/", response_model=List[VentaResponse])
def listar_ventas(
    skip: int = 0,
    limit: int = 100,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    usuario: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Listar ventas con filtros (solo admin)"""
    # Filtro base: solo hoy por defecto
    if not fecha_inicio and not fecha_fin:
        hoy = date.today()
        fecha_inicio = hoy
        fecha_fin = hoy
    
    query = db.query(Venta).join(Usuario, Venta.cliente_id == Usuario.id)
    
    # Filtro por fechas
    if fecha_inicio:
        inicio = datetime.combine(fecha_inicio, datetime.min.time())
        query = query.filter(Venta.fecha >= inicio)
    
    if fecha_fin:
        fin = datetime.combine(fecha_fin, datetime.max.time())
        query = query.filter(Venta.fecha <= fin)
    
    # Filtro por usuario
    if usuario:
        query = query.filter(
            (Usuario.nombre.ilike(f"%{usuario}%")) |
            (Usuario.correo.ilike(f"%{usuario}%"))
        )
    
    ventas = query.order_by(Venta.fecha.desc()).offset(skip).limit(limit).all()
    return ventas


@router.get("/total")
def total_ventas(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Obtener total de ventas por período"""
    if not fecha_inicio and not fecha_fin:
        hoy = date.today()
        fecha_inicio = hoy
        fecha_fin = hoy
    
    query = db.query(Venta)
    
    if fecha_inicio:
        inicio = datetime.combine(fecha_inicio, datetime.min.time())
        query = query.filter(Venta.fecha >= inicio)
    
    if fecha_fin:
        fin = datetime.combine(fecha_fin, datetime.max.time())
        query = query.filter(Venta.fecha <= fin)
    
    ventas = query.all()
    total = sum(venta.total for venta in ventas)
    
    return {
        "cantidad_ventas": len(ventas),
        "total": total,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }


@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Obtener venta por ID con detalles"""
    venta = db.query(Venta).filter(Venta.id == venta_id).first()
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    return venta


@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(
    venta_data: VentaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Crear nueva venta con detalles (solo admin)"""
    # Crear venta
    nueva_venta = Venta(
        cliente_id=venta_data.cliente_id,
        vendedor_id=venta_data.vendedor_id,
        trabajo_id=venta_data.trabajo_id,
        total=0
    )
    
    db.add(nueva_venta)
    db.flush()
    
    # Crear detalles
    total = 0
    for detalle_data in venta_data.detalles:
        detalle = DetalleVenta(
            **detalle_data.model_dump(),
            venta_id=nueva_venta.id
        )
        total += detalle.subtotal
        db.add(detalle)
    
    # Actualizar total
    nueva_venta.total = total
    
    db.commit()
    db.refresh(nueva_venta)
    
    return nueva_venta


@router.put("/{venta_id}", response_model=VentaResponse)
def actualizar_venta(
    venta_id: int,
    venta_data: VentaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Actualizar venta (solo admin)"""
    venta = db.query(Venta).filter(Venta.id == venta_id).first()
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    
    # Actualizar campos
    for field, value in venta_data.model_dump(exclude_unset=True).items():
        setattr(venta, field, value)
    
    db.commit()
    db.refresh(venta)
    
    return venta


@router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Eliminar venta (solo admin)"""
    venta = db.query(Venta).filter(Venta.id == venta_id).first()
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    
    db.delete(venta)
    db.commit()
    
    return None
