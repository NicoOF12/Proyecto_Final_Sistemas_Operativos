from models.filesystem.usuario import Usuario
from models.filesystem.directorio import Directorio

class SistemaArchivos:

    def __init__(self):
        self.usuarios = {
            "root": Usuario("root", 0, "root"),
            "usuario1": Usuario("usuario1", 1001, "usuarios"),
            "usuario2": Usuario("usuario2", 1002, "usuarios")
        }

        self.directorio_raiz = Directorio("/", self.usuarios["root"])
        self.usuario_actual = self.usuarios["root"]
        self.cwd = self.directorio_raiz   # Directorio actual

    # ---------- Helpers ----------
    def _obtener_directorio(self, ruta):
        partes = ruta.strip("/").split("/")
        actual = self.directorio_raiz

        for p in partes:
            if p == "":
                continue
            if p not in actual.subdirectorios:
                return None
            actual = actual.subdirectorios[p]

        return actual

    # ---------- Comandos ----------
    def mkdir(self, ruta):
        dirpadre = self._obtener_directorio("/")
        nombre = ruta.strip("/")
        dirpadre.crear_subdirectorio(nombre, self.usuario_actual)
        return f"Directorio '{nombre}' creado"

    def ls(self, ruta="/"):
        d = self._obtener_directorio(ruta)
        if not d:
            return "Directorio no encontrado"
        return {
            "directorios": list(d.subdirectorios.keys()),
            "archivos": list(d.archivos.keys())
        }

    def crear_archivo(self, ruta, contenido=""):
        nombre = ruta.strip("/")
        self.cwd.crear_archivo(nombre, self.usuario_actual)
        if contenido:
            self.cwd.archivos[nombre].escribir(contenido)
        return f"Archivo '{nombre}' creado"

    def leer_archivo(self, ruta):
        nombre = ruta.strip("/")
        if nombre not in self.cwd.archivos:
            return "Archivo no existe"
        return self.cwd.archivos[nombre].leer()

    def escribir_archivo(self, ruta, texto):
        nombre = ruta.strip("/")
        if nombre not in self.cwd.archivos:
            return "Archivo no existe"
        self.cwd.archivos[nombre].escribir(texto)
        return "Archivo modificado"

    def cd(self, ruta):
        d = self._obtener_directorio(ruta)
        if not d:
            return "Ruta no válida"
        self.cwd = d
        return f"Movido a {ruta}"
