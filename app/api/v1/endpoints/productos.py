from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_admin_user, get_current_active_user
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.schemas.producto import ProductoResponse, ProductoCreate, ProductoUpdate
from app.utils.files import save_upload_file

router = APIRouter()


@router.get("/", response_model=List[ProductoResponse])
def listar_productos(
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    categoria: Optional[str] = None,
    destacado: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Listar productos con filtros opcionales"""
    query = db.query(Producto)
    
    # Filtro por búsqueda de texto
    if q:
        query = query.filter(
            (Producto.nombre.ilike(f"%{q}%")) |
            (Producto.descripcion.ilike(f"%{q}%"))
        )
    
    # Filtro por categoría
    if categoria:
        query = query.filter(Producto.categoria == categoria)
    
    # Filtro por destacados
    if destacado is not None:
        query = query.filter(Producto.destacado == destacado)
    
    productos = query.offset(skip).limit(limit).all()
    return productos


@router.get("/categorias", response_model=List[str])
def listar_categorias(db: Session = Depends(get_db)):
    """Obtener lista de categorías únicas"""
    categorias = db.query(Producto.categoria).distinct().all()
    return [c[0] for c in categorias if c[0]]


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtener producto por ID"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    producto_data: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Crear nuevo producto (solo admin)"""
    new_producto = Producto(**producto_data.model_dump())
    
    db.add(new_producto)
    db.commit()
    db.refresh(new_producto)
    
    return new_producto


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto_data: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Actualizar producto (solo admin)"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Actualizar solo campos no nulos
    for field, value in producto_data.model_dump(exclude_unset=True).items():
        setattr(producto, field, value)
    
    db.commit()
    db.refresh(producto)
    
    return producto


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Eliminar producto (solo admin)"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    db.delete(producto)
    db.commit()
    
    return None


@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
def actualizar_stock(
    producto_id: int,
    cantidad: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Actualizar stock de producto"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    producto.stock = cantidad
    db.commit()
    db.refresh(producto)
    
    return producto
