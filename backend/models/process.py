from models.pcb import PCB

class Proceso:
    def __init__(self, pid, estado, contador, tiempo_llegada, rafaga_cpu, prioridad, registros, memoria, lista_archivos_abiertos, usuario):
        self.pcb = PCB(pid, "Nuevo", contador, tiempo_llegada, rafaga_cpu, prioridad, registros, memoria, lista_archivos_abiertos, usuario)

    def cambiar_Estado(self, nuevo_estado): # cambia el estado del proceso
        self.pcb.estado = nuevo_estado

    def ciclo_CPU(self): # simula un ciclo de CPU para el proceso
        if self.pcb.rafaga_CPU > 0:
            self.pcb.rafaga_CPU -= 1
            self.pcb.contador += 1
            if self.pcb.rafaga_CPU == 0:
                self.cambiar_Estado("Terminado")
        else:
            self.cambiar_Estado("Terminado")

    def __repr__(self): # retorna una cadena con los atributos del proceso
        return f"Proceso({self.pcb})"