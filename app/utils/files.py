import os
from datetime import datetime
from fastapi import UploadFile, HTTPException
from app.core.config import settings


def allowed_file(filename: str) -> bool:
    """Verificar si la extensión del archivo es permitida"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in settings.ALLOWED_EXTENSIONS


async def save_upload_file(file: UploadFile) -> str:
    """Guardar archivo subido y retornar nombre del archivo"""
    if not file:
        return None
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Crear carpeta si no existe
    upload_path = settings.UPLOAD_FOLDER
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    # Generar nombre único
    timestamp = datetime.now().timestamp()
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_path, filename)
    
    # Guardar archivo
    contents = await file.read()
    with open(file_path, 'wb') as f:
        f.write(contents)
    
    return filename


def delete_file(filename: str) -> bool:
    """Eliminar archivo"""
    if not filename:
        return False
    
    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
