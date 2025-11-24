from typing import Dict, Optional, Any
from .archivo import Archivo

class Directorio:
    def __init__(self, nombre: str, propietario: Any, permisos: str = "755", parent: Optional["Directorio"] = None):
        self.nombre = nombre
        self.propietario = propietario
        self.permisos = permisos  # numeric, e.g. "755"
        self.subdirectorios: Dict[str, "Directorio"] = {}
        self.archivos: Dict[str, Archivo] = {}
        self.parent = parent  # referencia al directorio padre (None si es root)

    def agregar_directorio(self, nombre: str, propietario: Any, permisos: str = "755") -> "Directorio":
        if nombre not in self.subdirectorios:
            d = Directorio(nombre, propietario, permisos=permisos, parent=self)
            self.subdirectorios[nombre] = d
        return self.subdirectorios[nombre]

    def agregar_archivo(self, archivo: Archivo):
        self.archivos[archivo.nombre] = archivo

    def quitar_archivo(self, nombre: str):
        if nombre in self.archivos:
            del self.archivos[nombre]

    def quitar_directorio(self, nombre: str):
        if nombre in self.subdirectorios:
            del self.subdirectorios[nombre]
