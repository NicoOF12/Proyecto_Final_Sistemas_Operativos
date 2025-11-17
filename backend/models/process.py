# models/process.py
from typing import Any, Dict, List, Optional
from models.pcb import PCB

class Proceso:
    """
    Clase Proceso que envuelve un PCB y agrega métodos de utilidad.
    Constructor detallado pero con valores por defecto para facilitar uso desde API.
    """

    def __init__(
        self,
        pid: int,
        tiempo_llegada: int = 0,
        rafaga_cpu: int = 1,
        usuario: str = "desconocido",
        prioridad: int = 1,
        estado: str = "Nuevo",
        registros: Optional[Dict[str, Any]] = None,
        memoria: Optional[Dict[str, Any]] = None,
        archivos_abiertos: Optional[List[str]] = None
    ):
        # Crear el PCB con los valores (PCB ya gestiona valores por defecto)
        self.pcb = PCB(
            pid=pid,
            estado=estado,
            contador=0,
            tiempo_llegada=tiempo_llegada,
            rafaga_cpu=rafaga_cpu,
            prioridad=prioridad,
            registros=registros,
            memoria=memoria,
            archivos_abiertos=archivos_abiertos,
            usuario=usuario
        )

        # Alias / atajos (opcional)
        self.tiempo_restante = self.pcb.tiempo_restante

    # Cambiar estado con validación
    def cambiar_estado(self, nuevo_estado: str) -> None:
        estados_validos = ["Nuevo", "Listo", "LISTO", "listo", "Ejecutando", "Ejecutando", "BLOQUEADO", "Bloqueado", "Terminado", "TERMINADO"]
        # Normalizar a formato capitalizado para consistencia
        mapping = {
            "listo": "Listo", "LISTO": "Listo", "Nuevo": "Nuevo", "nuevo": "Nuevo",
            "ejecutando": "Ejecutando", "EJECUTANDO": "Ejecutando",
            "bloqueado": "Bloqueado", "BLOQUEADO": "Bloqueado",
            "terminado": "Terminado", "TERMINADO": "Terminado"
        }
        nuevo = mapping.get(nuevo_estado, nuevo_estado)
        self.pcb.estado = nuevo

    def ciclo_cpu(self) -> None:
        """
        Simula un ciclo de CPU: decrementa tiempo_restante y actualiza contador/estado.
        Usa tiempo_restante (no rafaga_cpu) para compatibilidad con RR.
        """
        if self.pcb.tiempo_restante > 0:
            # Si es la primera vez que entra en CPU, fijar tiempo_inicio en el scheduler
            self.pcb.tiempo_restante -= 1
            self.pcb.contador += 1
            if self.pcb.tiempo_inicio is None:
                # tiempo_inicio será asignado desde el planificador al comenzar
                self.pcb.tiempo_inicio = None
            if self.pcb.tiempo_restante == 0:
                self.cambiar_estado("Terminado")
        else:
            self.cambiar_estado("Terminado")

    def reset(self) -> None:
        """Reinicia los campos dinámicos (útil en pruebas)."""
        self.pcb.tiempo_restante = self.pcb.rafaga_original
        self.pcb.tiempo_inicio = None
        self.pcb.tiempo_finalizacion = None
        self.pcb.tiempo_espera = 0
        self.pcb.tiempo_retorno = None
        self.pcb.contador = 0
        self.pcb.estado = "Nuevo"

    def to_dict(self) -> Dict[str, Any]:
        """Conveniencia: delega al PCB."""
        return self.pcb.to_dict()

    def __repr__(self) -> str:
        return f"Proceso(pid={self.pcb.pid}, estado={self.pcb.estado})"
