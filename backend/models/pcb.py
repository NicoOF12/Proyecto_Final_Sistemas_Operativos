class PCB:
    def __init__(self, PID, estado, contador, tiempo_llegada, rafaga_CPU, prioridad, registros, memoria, lista_archivos_abiertos, usuario):
        self.PID = PID # identificador único del proceso
        self.estado = estado # estado actual del proceso (e.g., 'listo', 'ejecutando', 'bloqueado')
        self.contador = contador # contador de programa del proceso
        self.tiempo_llegada = tiempo_llegada # tiempo en que el proceso llegó al sistema
        self.rafaga_CPU = rafaga_CPU # tiempo de CPU requerido por el proceso
        self.prioridad = prioridad # prioridad del proceso
        self.registros = registros  # Diccionario para almacenar los registros del proceso
        self.memoria = memoria      # Información de memoria asignada al proceso
        self.lista_archivos_abiertos = lista_archivos_abiertos  # Lista de archivos abiertos por el proceso
        self.usuario = usuario    # Usuario asociado al proceso

    def __repr__(self): # retorna una cadena con los atributos del PCB
        return (f"PCB(PID={self.PID}, estado={self.estado}, contador={self.contador}, "
                f"tiempo_llegada={self.tiempo_llegada}, rafaga_CPU={self.rafaga_CPU}, "
                f"prioridad={self.prioridad}, registros={self.registros}, memoria={self.memoria}, "
                f"lista_archivos_abiertos={self.lista_archivos_abiertos}, usuario={self.usuario})")
    
    def diccionario(self): # retorna un diccionario con los atributos del PCB
        return {
            "PID": self.PID,
            "estado": self.estado,
            "contador": self.contador,
            "tiempo_llegada": self.tiempo_llegada,
            "rafaga_CPU": self.rafaga_CPU,
            "prioridad": self.prioridad,
            "registros": self.registros,
            "memoria": self.memoria,
            "lista_archivos_abiertos": self.lista_archivos_abiertos,
            "usuario": self.usuario
        }