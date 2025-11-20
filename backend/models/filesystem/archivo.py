from typing import Any

class Archivo:
    def __init__(self, nombre: str, propietario: Any, permisos: str = "644"):
        self.nombre = nombre
        self.propietario = propietario   # Usuario
        self.permisos = permisos         # "644" (numeric)
        self.contenido = ""
        self.tamanio = 0

    def escribir(self, texto: str):
        self.contenido = texto
        self.tamanio = len(texto)

    def leer(self) -> str:
        return self.contenido
