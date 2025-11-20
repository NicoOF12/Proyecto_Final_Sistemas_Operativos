from typing import Optional

class Usuario:
    def __init__(self, nombre: str, uid: int, grupo: str, password: Optional[str] = None):
        self.nombre = nombre
        self.uid = uid
        self.grupo = grupo
        self.password = password  # opcional: no usado en esta simulación simple

    def __repr__(self):
        return f"Usuario({self.nombre}, uid={self.uid}, grupo={self.grupo})"
