class Usuario:
    def __init__(self, nombre: str, uid: int, grupo: str):
        self.nombre = nombre
        self.uid = uid
        self.grupo = grupo

    def __repr__(self):
        return f"Usuario({self.nombre}, uid={self.uid}, grupo={self.grupo})"
