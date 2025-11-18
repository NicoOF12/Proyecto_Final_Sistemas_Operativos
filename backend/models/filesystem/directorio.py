from models.filesystem.archivo import Archivo

class Directorio:
    def __init__(self, nombre, propietario):
        self.nombre = nombre
        self.propietario = propietario
        self.subdirectorios = {}   # {"docs": Directorio, ...}
        self.archivos = {}         # {"notas.txt": Archivo, ...}

    def crear_subdirectorio(self, nombre, propietario):
        self.subdirectorios[nombre] = Directorio(nombre, propietario)

    def crear_archivo(self, nombre, propietario, permisos="644"):
        self.archivos[nombre] = Archivo(nombre, propietario, permisos)
