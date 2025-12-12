# Taller Mecánico - Backend FastAPI

Backend API REST desarrollado en FastAPI para sistema de gestión de taller mecánico. Migrado desde Flask con la misma base de datos y funcionalidad.

## 🚀 Características

- ✅ Autenticación JWT (login/registro)
- ✅ Gestión de usuarios con roles (admin, mecanico, usuario)
- ✅ CRUD completo de productos con categorías
- ✅ Sistema de trabajos con estados
- ✅ Ventas y detalles de venta
- ✅ Gestión de gastos
- ✅ Dashboard con estadísticas
- ✅ Subida de archivos (imágenes)
- ✅ Filtros avanzados
- ✅ Validación con Pydantic
- ✅ Documentación automática (Swagger/OpenAPI)

## 📋 Requisitos

- Python 3.11+
- MySQL 8.0+
- pip o poetry

## 🔧 Instalación

### 1. Clonar e instalar dependencias

\`\`\`bash
cd fastapi_backend
pip install -r requirements.txt
\`\`\`

### 2. Configurar variables de entorno

Copiar `.env.example` a `.env` y configurar:

\`\`\`bash
cp .env.example .env
\`\`\`

Editar `.env` con tus credenciales de base de datos:

\`\`\`env
DATABASE_URI=mysql+pymysql://usuario:password@localhost:3306/taller_mecanico
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura
\`\`\`

### 3. Base de datos

La base de datos ya debe estar creada con el schema del proyecto Flask. Si no, ejecutar el SQL proporcionado.

### 4. Ejecutar servidor

\`\`\`bash
# Desarrollo
python main.py

# O con uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

El servidor estará disponible en: `http://localhost:8000`

## 📚 Documentación API

Una vez iniciado el servidor, acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Autenticación

### Registro
\`\`\`bash
POST /api/v1/auth/registro
{
  "correo": "user@example.com",
  "contraseña": "password123",
  "nombre": "Juan Pérez",
  "rol": "usuario"
}
\`\`\`

### Login
\`\`\`bash
POST /api/v1/auth/login
{
  "correo": "user@example.com",
  "contraseña": "password123"
}
\`\`\`

Retorna un token JWT que debe enviarse en el header `Authorization: Bearer <token>` para endpoints protegidos.

## 📡 Endpoints Principales

### Usuarios
- `GET /api/v1/usuarios/` - Listar usuarios (admin)
- `POST /api/v1/usuarios/` - Crear usuario (admin)
- `PUT /api/v1/usuarios/{id}` - Actualizar usuario (admin)
- `DELETE /api/v1/usuarios/{id}` - Eliminar usuario (admin)
- `GET /api/v1/usuarios/rol/{rol}` - Listar por rol (admin)

### Productos
- `GET /api/v1/productos/` - Listar productos (público)
- `GET /api/v1/productos/{id}` - Obtener producto (público)
- `POST /api/v1/productos/` - Crear producto (admin)
- `PUT /api/v1/productos/{id}` - Actualizar producto (admin)
- `DELETE /api/v1/productos/{id}` - Eliminar producto (admin)
- `GET /api/v1/productos/categorias` - Listar categorías

### Trabajos
- `GET /api/v1/trabajos/` - Listar trabajos (según rol)
- `POST /api/v1/trabajos/` - Crear trabajo (admin/mecanico)
- `PUT /api/v1/trabajos/{id}` - Actualizar trabajo
- `PATCH /api/v1/trabajos/{id}/estado` - Cambiar estado
- `DELETE /api/v1/trabajos/{id}` - Eliminar trabajo (admin)
- `GET /api/v1/trabajos/estadisticas` - Estadísticas (admin)

### Ventas
- `GET /api/v1/ventas/` - Listar ventas (admin)
- `POST /api/v1/ventas/` - Crear venta (admin)
- `PUT /api/v1/ventas/{id}` - Actualizar venta (admin)
- `DELETE /api/v1/ventas/{id}` - Eliminar venta (admin)
- `GET /api/v1/ventas/total` - Total de ventas por período

### Gastos
- `GET /api/v1/gastos/` - Listar gastos (admin)
- `POST /api/v1/gastos/` - Crear gasto (admin)
- `PUT /api/v1/gastos/{id}` - Actualizar gasto (admin)
- `DELETE /api/v1/gastos/{id}` - Eliminar gasto (admin)
- `GET /api/v1/gastos/total` - Total de gastos por período

### Dashboard
- `GET /api/v1/dashboard/admin` - Dashboard admin
- `GET /api/v1/dashboard/mecanico` - Dashboard mecánico
- `GET /api/v1/dashboard/usuario` - Dashboard usuario

## 🐳 Docker

### Construir y ejecutar con Docker Compose

\`\`\`bash
docker-compose up -d
\`\`\`

Esto levantará:
- API en puerto 8000
- MySQL en puerto 3306

## 🧪 Testing

Para probar los endpoints, usar la documentación interactiva en `/docs` o herramientas como:
- Postman
- Insomnia
- curl
- httpie

## 🔄 Migración desde Flask

Este backend mantiene:
- ✅ Misma estructura de base de datos
- ✅ Mismos modelos (Usuario, Producto, Trabajo, Venta, Gasto)
- ✅ Misma lógica de negocio
- ✅ Roles y permisos equivalentes

**Cambios principales:**
- 🔄 Sesiones de Flask → JWT tokens
- 🔄 Flask-Login → FastAPI dependencies
- 🔄 Templates HTML → API JSON (sin vistas)
- 🔄 Blueprints → Routers
- 🔄 WTForms → Pydantic schemas

## 📁 Estructura del Proyecto

\`\`\`
fastapi_backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── usuarios.py
│   │       │   ├── productos.py
│   │       │   ├── trabajos.py
│   │       │   ├── ventas.py
│   │       │   ├── gastos.py
│   │       │   └── dashboard.py
│   │       └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── deps.py
│   ├── models/
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   ├── trabajo.py
│   │   ├── venta.py
│   │   └── gasto.py
│   ├── schemas/
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   ├── trabajo.py
│   │   ├── venta.py
│   │   └── gasto.py
│   └── utils/
│       └── files.py
├── uploads/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
\`\`\`

## 🤝 Contribuir

Este backend está listo para conectarse con cualquier frontend (Flutter, React, Vue, etc.)

## 📝 Licencia

Proyecto privado para taller mecánico.
