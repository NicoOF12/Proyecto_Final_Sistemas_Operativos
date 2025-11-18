from fastapi import APIRouter
from models.filesystem.sistema_de_archivos import SistemaArchivos

router = APIRouter(prefix="/fs", tags=["Sistema de Archivos"])

fs = SistemaArchivos()

@router.get("/ls")
def listar(ruta: str = "/"):
    return fs.ls(ruta)

@router.post("/mkdir")
def crear_dir(ruta: str):
    return fs.mkdir(ruta)

@router.post("/create")
def crear_archivo(ruta: str, contenido: str = ""):
    return fs.crear_archivo(ruta, contenido)

@router.get("/read")
def leer_archivo(ruta: str):
    return fs.leer_archivo(ruta)

@router.post("/write")
def escribir_archivo(ruta: str, texto: str):
    return fs.escribir_archivo(ruta, texto)

@router.post("/cd")
def cambiar_directorio(ruta: str):
    return fs.cd(ruta)
