from typing import Optional, Tuple, List, Dict, Any
from .usuario import Usuario
from .directorio import Directorio
from .archivo import Archivo

# ---------- helpers permisos ----------
_NUM_TO_RWX = {
    '7': 'rwx', '6': 'rw-', '5': 'r-x', '4': 'r--',
    '3': '-wx', '2': '-w-', '1': '--x', '0': '---'
}

def numeric_to_rwx(numeric: str) -> str:
    n = str(numeric).zfill(3)[-3:]
    return ''.join(_NUM_TO_RWX[d] for d in n)

def can_access(user: Usuario, owner: Usuario, owner_group: str, perm_numeric: str, mode: str) -> bool:
    """
    mode: 'r'|'w'|'x'
    reglas:
      - root (uid==0) -> siempre true
      - si user==owner -> primer dígito
      - elif user.grupo == owner_group -> segundo dígito
      - else -> tercero
    """
    if user.uid == 0:
        return True

    perm_numeric = str(perm_numeric).zfill(3)[-3:]
    owner_dig = int(perm_numeric[0])
    group_dig = int(perm_numeric[1])
    other_dig = int(perm_numeric[2])

    if user.nombre == owner.nombre:
        digit = owner_dig
    elif user.grupo == owner_group:
        digit = group_dig
    else:
        digit = other_dig

    if mode == 'r':
        return bool(digit & 4)
    if mode == 'w':
        return bool(digit & 2)
    if mode == 'x':
        return bool(digit & 1)
    return False

# ---------- Sistema de archivos ----------
class SistemaArchivos:
    def __init__(self):
        # usuarios de ejemplo
        self.usuarios: Dict[str, Usuario] = {
            "root": Usuario("root", 0, "root"),
            "usuario1": Usuario("usuario1", 1001, "usuarios"),
            "usuario2": Usuario("usuario2", 1002, "usuarios")
        }

        # root con permisos 777 (todos pueden escribir)
        self.root = Directorio("/", self.usuarios["root"], permisos="777", parent=None)
        
        # crear /home con permisos 777 (todos pueden crear directorios)
        home = self.root.agregar_directorio("home", self.usuarios["root"], permisos="777")
        
        # Directorios de usuarios con permisos 755 (propietario: rwx, grupo: rx, otros: rx)
        u1 = home.agregar_directorio("usuario1", self.usuarios["usuario1"], permisos="755")
        u2 = home.agregar_directorio("usuario2", self.usuarios["usuario2"], permisos="755")

        # estado actual
        self.usuario_actual: Usuario = self.usuarios["root"]
        self.cwd: Directorio = self.root
        self.cwd_path: str = "/"

    # -------------- RUTAS & RESOLUCIÓN --------------
    def _ruta_a_partes(self, ruta: str) -> List[str]:
        if ruta is None:
            return []
        r = ruta.strip()
        if r == "" or r == "/":
            return []
        if r.startswith("/"):
            r = r[1:]
        partes = [p for p in r.split("/") if p != ""]
        return partes

    def _obtener_dir_por_ruta(self, ruta: str) -> Optional[Directorio]:
        """
        Soporta rutas absolutas y relativas, y los componentes '.' y '..'
        """
        if ruta is None or ruta.strip() == "" or ruta == ".":
            return self.cwd
        if ruta == "/":
            return self.root

        partes = self._ruta_a_partes(ruta)
        # seleccionar punto de inicio
        actual = self.root if ruta.startswith("/") else self.cwd

        for p in partes:
            if p == ".":
                continue
            if p == "..":
                actual = actual.parent if actual.parent is not None else actual
                continue
            if p not in actual.subdirectorios:
                return None
            actual = actual.subdirectorios[p]
        return actual

    def _resolve_parent_and_name(self, ruta: str) -> Tuple[Optional[Directorio], Optional[str]]:
        """
        devuelve (directorio_padre, nombre)
        """
        if ruta is None or ruta.strip() == "":
            return (self.cwd, None)
        partes = self._ruta_a_partes(ruta)
        if ruta.startswith("/"):
            if len(partes) == 0:
                return (self.root, None)
            if len(partes) == 1:
                return (self.root, partes[0])
            parent_path = "/" + "/".join(partes[:-1])
            parent = self._obtener_dir_por_ruta(parent_path)
            return (parent, partes[-1])
        else:
            if len(partes) == 1:
                return (self.cwd, partes[0])
            parent = self._obtener_dir_por_ruta("/".join(partes[:-1]))
            return (parent, partes[-1])

    # ---------------- USUARIO ----------------
    def su(self, username: str) -> dict:
        if username not in self.usuarios:
            return {"error": "usuario no existe"}
        self.usuario_actual = self.usuarios[username]
        # cuando cambias de usuario, por simplicidad no cambiamos cwd salvo si pasas a root -> dejar igual.
        return {"ok": f"usuario actual: {username}"}

    # ---------------- NAVEGACIÓN / INFO ----------------
    def pwd(self) -> str:
        # reconstruye path desde cwd
        node = self.cwd
        if node.parent is None:
            return "/"
        partes = []
        while node.parent is not None:
            partes.append(node.nombre)
            node = node.parent
        return "/" + "/".join(reversed(partes))

    def ls(self, ruta: str = ".") -> dict:
        dir_obj = self._obtener_dir_por_ruta(ruta)
        if dir_obj is None:
            return {"error": "Directorio no encontrado"}
        # verificar permiso de lectura de ese directorio
        if not can_access(self.usuario_actual, dir_obj.propietario, dir_obj.propietario.grupo, dir_obj.permisos, 'r'):
            return {"error": "permiso denegado para listar este directorio"}
        directorios = []
        archivos = []
        for name, d in dir_obj.subdirectorios.items():
            directorios.append({
                "nombre": name,
                "propietario": d.propietario.nombre,
                "permisos": d.permisos,
            })
        for name, f in dir_obj.archivos.items():
            archivos.append({
                "nombre": name,
                "propietario": f.propietario.nombre,
                "permisos": f.permisos,
                "tamanio": f.tamanio
            })
        return {"path": self.pwd() if ruta == "." else ruta, "directorios": directorios, "archivos": archivos}

    def mkdir(self, ruta: str, permisos: str = "755") -> dict:
        parent, nombre = self._resolve_parent_and_name(ruta)
        if parent is None or nombre is None:
            return {"error": "ruta inválida"}
        
        # Verificar si ya existe
        if nombre in parent.subdirectorios:
            return {"error": f"El directorio '{nombre}' ya existe"}
        
        # escribir en parent: permiso w
        if not can_access(self.usuario_actual, parent.propietario, parent.propietario.grupo, parent.permisos, 'w'):
            return {"error": f"permiso denegado para crear en {self.pwd()}. Usuario: {self.usuario_actual.nombre}, Propietario: {parent.propietario.nombre}, Permisos: {parent.permisos}"}
        
        parent.agregar_directorio(nombre, self.usuario_actual, permisos=permisos)
        return {"ok": f"Directorio '{nombre}' creado", "permisos": permisos}

    def cd(self, ruta: str) -> dict:
        dir_obj = self._obtener_dir_por_ruta(ruta)
        if dir_obj is None:
            return {"error": "ruta inválida"}
        # permiso de ejecución (x) para entrar
        if not can_access(self.usuario_actual, dir_obj.propietario, dir_obj.propietario.grupo, dir_obj.permisos, 'x'):
            return {"error": "permiso denegado para entrar a ese directorio"}
        self.cwd = dir_obj
        self.cwd_path = self.pwd()
        return {"ok": f"cd -> {self.cwd_path}"}

    # ---------------- ARCHIVOS ----------------
    def crear_archivo(self, ruta: str, contenido: str = "", permisos: str = "644") -> dict:
        parent, nombre = self._resolve_parent_and_name(ruta)
        if parent is None or nombre is None:
            return {"error": "ruta inválida"}
        
        # Verificar si ya existe
        if nombre in parent.archivos:
            return {"error": f"El archivo '{nombre}' ya existe"}
        
        # permiso de escritura en parent
        if not can_access(self.usuario_actual, parent.propietario, parent.propietario.grupo, parent.permisos, 'w'):
            return {"error": f"permiso denegado para crear archivo en {self.pwd()}"}
        
        archivo = Archivo(nombre, self.usuario_actual, permisos=permisos)
        if contenido:
            archivo.escribir(contenido)
        parent.agregar_archivo(archivo)
        return {"ok": f"Archivo '{nombre}' creado", "permisos": permisos}

    def read(self, ruta: str) -> dict:
        parent, nombre = self._resolve_parent_and_name(ruta)
        if parent is None or nombre is None or nombre not in parent.archivos:
            return {"error": "archivo no encontrado"}
        archivo = parent.archivos[nombre]
        # permiso lectura
        if not can_access(self.usuario_actual, archivo.propietario, archivo.propietario.grupo, archivo.permisos, 'r'):
            return {"error": "permiso denegado para leer"}
        return {"contenido": archivo.leer()}

    def write(self, ruta: str, texto: str) -> dict:
        parent, nombre = self._resolve_parent_and_name(ruta)
        if parent is None or nombre is None or nombre not in parent.archivos:
            return {"error": "archivo no encontrado"}
        archivo = parent.archivos[nombre]
        # permiso escritura
        if not can_access(self.usuario_actual, archivo.propietario, archivo.propietario.grupo, archivo.permisos, 'w'):
            return {"error": "permiso denegado para escribir"}
        archivo.escribir(texto)
        return {"ok": "archivo modificado"}

    def rm(self, ruta: str) -> dict:
        parent, nombre = self._resolve_parent_and_name(ruta)
        if parent is None or nombre is None:
            return {"error": "ruta inválida"}
        # si existe archivo
        if nombre in parent.archivos:
            archivo = parent.archivos[nombre]
            # permiso escritura en parent o ser propietario/root
            if not can_access(self.usuario_actual, parent.propietario, parent.propietario.grupo, parent.permisos, 'w'):
                return {"error": "permiso denegado para eliminar"}
            parent.quitar_archivo(nombre)
            return {"ok": f"Archivo '{nombre}' eliminado"}
        # si es subdirectorio
        if nombre in parent.subdirectorios:
            d = parent.subdirectorios[nombre]
            # debe estar vacío
            if d.subdirectorios or d.archivos:
                return {"error": "directorio no vacío"}
            if not can_access(self.usuario_actual, parent.propietario, parent.propietario.grupo, parent.permisos, 'w'):
                return {"error": "permiso denegado para eliminar directorio"}
            parent.quitar_directorio(nombre)
            return {"ok": f"Directorio '{nombre}' eliminado"}
        return {"error": "no existe"}

    def chmod(self, ruta: str, permisos: str) -> dict:
        parent, nombre = self._resolve_parent_and_name(ruta)
        # si nombre es None significa que ruta apunta a un directorio directo (o '/')
        if parent is None:
            return {"error": "ruta inválida"}
        if nombre is None:
            # cambiar permisos del parent
            dir_obj = parent
            if self.usuario_actual.nombre != dir_obj.propietario.nombre and self.usuario_actual.uid != 0:
                return {"error": "permiso denegado para chmod en directorio"}
            dir_obj.permisos = permisos
            return {"ok": f"permisos de directorio cambiados a {permisos}"}
        # archivo
        if nombre in parent.archivos:
            archivo = parent.archivos[nombre]
            if self.usuario_actual.nombre != archivo.propietario.nombre and self.usuario_actual.uid != 0:
                return {"error": "solo propietario o root puede cambiar permisos"}
            archivo.permisos = permisos
            return {"ok": f"permisos de '{nombre}' cambiados a {permisos}"}
        # subdir
        if nombre in parent.subdirectorios:
            dir_obj = parent.subdirectorios[nombre]
            if self.usuario_actual.nombre != dir_obj.propietario.nombre and self.usuario_actual.uid != 0:
                return {"error": "solo propietario o root puede cambiar permisos en subdirectorio"}
            dir_obj.permisos = permisos
            return {"ok": f"permisos del directorio '{nombre}' a {permisos}"}
        return {"error": "no existe"}

    def chown(self, ruta: str, nuevo: str) -> dict:
        parent, nombre = self._resolve_parent_and_name(ruta)
        if parent is None or nombre is None:
            return {"error": "ruta inválida"}
        if nuevo not in self.usuarios:
            return {"error": "nuevo propietario no existe"}
        nuevo_user = self.usuarios[nuevo]
        if nombre in parent.archivos:
            archivo = parent.archivos[nombre]
            if self.usuario_actual.uid != 0:
                return {"error": "solo root puede chown"}
            archivo.propietario = nuevo_user
            return {"ok": f"propietario de '{nombre}' ahora {nuevo}"}
        if nombre in parent.subdirectorios:
            d = parent.subdirectorios[nombre]
            if self.usuario_actual.uid != 0:
                return {"error": "solo root puede chown en directorios"}
            d.propietario = nuevo_user
            return {"ok": f"propietario del directorio '{nombre}' ahora {nuevo}"}
        return {"error": "no existe"}

    # util que lista usuarios (para tests)
    def listar_usuarios(self) -> List[str]:
        return list(self.usuarios.keys())