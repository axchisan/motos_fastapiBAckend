from fastapi import APIRouter
from app.api.v1.endpoints import auth, usuarios, productos, trabajos, ventas, gastos, dashboard

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(productos.router, prefix="/productos", tags=["Productos"])
api_router.include_router(trabajos.router, prefix="/trabajos", tags=["Trabajos"])
api_router.include_router(ventas.router, prefix="/ventas", tags=["Ventas"])
api_router.include_router(gastos.router, prefix="/gastos", tags=["Gastos"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
