from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, date

from app.core.database import get_db
from app.core.deps import get_admin_user, get_mecanico_user, get_cliente_user
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.models.trabajo import Trabajo
from app.models.venta import Venta
from app.models.gasto import Gasto

router = APIRouter()


@router.get("/admin")
def dashboard_admin(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Dashboard completo para administrador"""
    # Estadísticas generales
    stats = {
        "usuarios": db.query(Usuario).count(),
        "productos": db.query(Producto).count(),
        "trabajos": db.query(Trabajo).count(),
        "ventas": db.query(Venta).count()
    }
    
    # Conteo por rol
    roles_count = {
        "admin": db.query(Usuario).filter(Usuario.rol == "admin").count(),
        "mecanico": db.query(Usuario).filter(Usuario.rol == "mecanico").count(),
        "usuario": db.query(Usuario).filter(Usuario.rol == "usuario").count()
    }
    
    # Productos por categoría
    categorias = db.query(Producto.categoria, func.count(Producto.id))\
        .group_by(Producto.categoria)\
        .all()
    
    # Trabajos últimos 5 días
    hoy = date.today()
    trabajos_dias = []
    for i in range(5):
        fecha = hoy - timedelta(days=4-i)
        count = db.query(Trabajo).filter(
            func.date(Trabajo.fecha_creacion) == fecha
        ).count()
        trabajos_dias.append({
            "fecha": fecha.strftime('%d/%m'),
            "cantidad": count
        })
    
    # Ventas últimos 7 días
    ventas_dias = []
    for i in range(7):
        fecha = hoy - timedelta(days=6-i)
        ventas = db.query(Venta).filter(
            func.date(Venta.fecha) == fecha
        ).all()
        total = sum(v.total for v in ventas)
        ventas_dias.append({
            "fecha": fecha.strftime('%d/%m'),
            "cantidad": len(ventas),
            "total": total
        })
    
    return {
        "stats": stats,
        "roles": roles_count,
        "categorias": [{"nombre": c[0], "cantidad": c[1]} for c in categorias if c[0]],
        "trabajos_dias": trabajos_dias,
        "ventas_dias": ventas_dias
    }


@router.get("/mecanico")
def dashboard_mecanico(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_mecanico_user)
):
    """Dashboard para mecánico"""
    # Trabajos asignados
    trabajos = db.query(Trabajo).filter(
        Trabajo.mecanico_id == current_user.id
    ).all()
    
    # Estadísticas por estado
    stats = {
        "total": len(trabajos),
        "pendientes": len([t for t in trabajos if t.estado == "pendiente"]),
        "en_proceso": len([t for t in trabajos if t.estado == "en proceso"]),
        "completados": len([t for t in trabajos if t.estado == "completado"]),
        "pagados": len([t for t in trabajos if t.estado == "pagado"])
    }
    
    return {
        "stats": stats,
        "trabajos_recientes": trabajos[:10]
    }


@router.get("/usuario")
def dashboard_usuario(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_cliente_user)
):
    """Dashboard para usuario/cliente"""
    # Trabajos del cliente
    trabajos = db.query(Trabajo).filter(
        Trabajo.cliente_id == current_user.id
    ).all()
    
    # Compras del cliente
    compras = db.query(Venta).filter(
        Venta.cliente_id == current_user.id
    ).all()
    
    return {
        "trabajos": {
            "total": len(trabajos),
            "pendientes": len([t for t in trabajos if t.estado == "pendiente"]),
            "completados": len([t for t in trabajos if t.estado == "completado"])
        },
        "compras": {
            "total": len(compras),
            "monto_total": sum(c.total for c in compras)
        }
    }
