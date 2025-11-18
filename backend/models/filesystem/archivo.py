class Archivo:
    def __init__(self, nombre, propietario, permisos="644"):
        self.nombre = nombre
        self.propietario = propietario  # Usuario
        self.permisos = permisos        # "rw-r--r--"
        self.contenido = ""
        self.tamano = 0

    def escribir(self, texto):
        self.contenido = texto
        self.tamano = len(texto)

    def leer(self):
        return self.contenido
