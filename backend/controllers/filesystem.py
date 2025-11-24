from fastapi import APIRouter
from models.filesystem.sistema_de_archivos import SistemaArchivos

router = APIRouter(prefix="/fs", tags=["filesystem"])
fs = SistemaArchivos()

@router.post("/su")
def su(username: str):
    return fs.su(username)

@router.get("/pwd")
def pwd():
    return {"pwd": fs.pwd()}

@router.get("/ls")
def ls(ruta: str = "."):
    return fs.ls(ruta)

@router.post("/mkdir")
def mkdir(ruta: str, permisos: str = "755"):
    return fs.mkdir(ruta, permisos=permisos)

@router.post("/cd")
def cd(ruta: str):
    return fs.cd(ruta)

@router.post("/create")
def create(ruta: str, contenido: str = "", permisos: str = "644"):
    return fs.crear_archivo(ruta, contenido, permisos=permisos)

@router.get("/read")
def read(ruta: str):
    return fs.read(ruta)

@router.post("/write")
def write(ruta: str, contenido: str):
    return fs.write(ruta, contenido)

@router.post("/rm")
def rm(ruta: str):
    return fs.rm(ruta)

@router.post("/chmod")
def chmod(ruta: str, permisos: str):
    return fs.chmod(ruta, permisos)

@router.post("/chown")
def chown(ruta: str, nuevo_propietario: str):
    return fs.chown(ruta, nuevo_propietario)

@router.get("/users")
def users():
    return {"users": fs.listar_usuarios()}
