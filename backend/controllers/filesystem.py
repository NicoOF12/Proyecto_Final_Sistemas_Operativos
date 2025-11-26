from fastapi import APIRouter, Depends, HTTPException
from models.filesystem.sistema_de_archivos import SistemaArchivos

router = APIRouter(prefix="/fs", tags=["filesystem"])

# Instancia global del sistema de archivos
_fs_instance = SistemaArchivos()

def get_fs():
    """Dependency que retorna la instancia del filesystem"""
    return _fs_instance

@router.post("/su")
def su(username: str, fs: SistemaArchivos = Depends(get_fs)):
    result = fs.su(username)
    return result

@router.get("/pwd")
def pwd(fs: SistemaArchivos = Depends(get_fs)):
    return {"pwd": fs.pwd()}

@router.get("/ls")
def ls(ruta: str = ".", fs: SistemaArchivos = Depends(get_fs)):
    result = fs.ls(ruta)
    
    # Si hay error, retornar tal cual
    if "error" in result:
        return result
    
    # Transformar el formato para el frontend
    contenido = []
    
    # Agregar directorios
    for dir_info in result.get("directorios", []):
        contenido.append({
            "nombre": dir_info["nombre"],
            "tipo": "directorio",
            "propietario": dir_info["propietario"],
            "permisos": dir_info["permisos"]
        })
    
    # Agregar archivos
    for file_info in result.get("archivos", []):
        contenido.append({
            "nombre": file_info["nombre"],
            "tipo": "archivo",
            "propietario": file_info["propietario"],
            "permisos": file_info["permisos"],
            "tamanio": file_info.get("tamanio", 0)
        })
    
    return {
        "path": result.get("path", ruta),
        "contenido": contenido
    }

@router.post("/mkdir")
def mkdir(ruta: str, permisos: str = "755", fs: SistemaArchivos = Depends(get_fs)):
    result = fs.mkdir(ruta, permisos=permisos)
    print(f"[DEBUG] mkdir result: {result}")  # Debug
    return result

@router.post("/cd")
def cd(ruta: str, fs: SistemaArchivos = Depends(get_fs)):
    result = fs.cd(ruta)
    print(f"[DEBUG] cd result: {result}")  # Debug
    return result

@router.post("/create")
def create(ruta: str, contenido: str = "", permisos: str = "644", fs: SistemaArchivos = Depends(get_fs)):
    result = fs.crear_archivo(ruta, contenido, permisos=permisos)
    print(f"[DEBUG] create file result: {result}")  # Debug
    return result

@router.get("/read")
def read(ruta: str, fs: SistemaArchivos = Depends(get_fs)):
    return fs.read(ruta)

@router.post("/write")
def write(ruta: str, contenido: str, fs: SistemaArchivos = Depends(get_fs)):
    return fs.write(ruta, contenido)

@router.post("/rm")
def rm(ruta: str, fs: SistemaArchivos = Depends(get_fs)):
    result = fs.rm(ruta)
    print(f"[DEBUG] rm result: {result}")  # Debug
    return result

@router.post("/chmod")
def chmod(ruta: str, permisos: str, fs: SistemaArchivos = Depends(get_fs)):
    return fs.chmod(ruta, permisos)

@router.post("/chown")
def chown(ruta: str, nuevo_propietario: str, fs: SistemaArchivos = Depends(get_fs)):
    return fs.chown(ruta, nuevo_propietario)

@router.get("/users")
def users(fs: SistemaArchivos = Depends(get_fs)):
    return {"users": fs.listar_usuarios()}

@router.get("/current-user")
def current_user(fs: SistemaArchivos = Depends(get_fs)):
    """Endpoint para obtener el usuario actual"""
    return {
        "username": fs.usuario_actual.nombre,
        "uid": fs.usuario_actual.uid,
        "grupo": fs.usuario_actual.grupo
    }

@router.get("/debug/tree")
def debug_tree(fs: SistemaArchivos = Depends(get_fs)):
    """Endpoint de debug para ver toda la estructura del filesystem"""
    def build_tree(dir_obj, path="/"):
        tree = {
            "path": path,
            "owner": dir_obj.propietario.nombre,
            "permisos": dir_obj.permisos,
            "subdirs": {},
            "files": []
        }
        for name, subdir in dir_obj.subdirectorios.items():
            tree["subdirs"][name] = build_tree(subdir, f"{path}{name}/")
        for name, archivo in dir_obj.archivos.items():
            tree["files"].append({
                "nombre": name,
                "owner": archivo.propietario.nombre,
                "permisos": archivo.permisos,
                "tamanio": archivo.tamanio
            })
        return tree
    
    return {
        "current_user": fs.usuario_actual.nombre,
        "current_path": fs.pwd(),
        "tree": build_tree(fs.root)
    }