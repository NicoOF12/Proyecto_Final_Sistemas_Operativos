# models/pcb.py
from typing import Any, Dict, List, Optional

class PCB:
    """
    Bloque de control de proceso (PCB) con campos completos.
    Todos los campos tienen valores por defecto para facilitar la creación.
    """

    def __init__(
        self,
        pid: int,
        estado: str = "Nuevo",
        contador: int = 0,
        tiempo_llegada: int = 0,
        rafaga_cpu: int = 1,
        prioridad: int = 1,
        registros: Optional[Dict[str, Any]] = None,
        memoria: Optional[Dict[str, Any]] = None,
        archivos_abiertos: Optional[List[str]] = None,
        usuario: str = "desconocido"
    ):
        if registros is None:
            registros = {}
        if memoria is None:
            memoria = {}
        if archivos_abiertos is None:
            archivos_abiertos = []

        # Campos básicos
        self.pid: int = pid
        self.estado: str = estado
        self.contador: int = contador
        self.tiempo_llegada: int = tiempo_llegada
        self.rafaga_cpu: int = rafaga_cpu
        self.prioridad: int = prioridad
        self.registros: Dict[str, Any] = registros
        self.memoria: Dict[str, Any] = memoria
        self.archivos_abiertos: List[str] = archivos_abiertos
        self.usuario: str = usuario

        # Campos para métricas / simulación
        self.tiempo_restante: int = rafaga_cpu           # útil para Round Robin
        self.rafaga_original: int = rafaga_cpu            # para métricas y visualización
        self.tiempo_inicio: Optional[int] = None          # primer instante en CPU
        self.tiempo_finalizacion: Optional[int] = None   # cuando termina
        self.tiempo_espera: int = 0                       # acumulado en ready
        self.tiempo_retorno: Optional[int] = None         # turnaround = finalizacion - llegada

    def to_dict(self) -> Dict[str, Any]:
        """Representación JSON-friendly del PCB."""
        return {
            "pid": self.pid,
            "estado": self.estado,
            "contador": self.contador,
            "tiempo_llegada": self.tiempo_llegada,
            "rafaga_cpu": self.rafaga_cpu,
            "rafaga_original": self.rafaga_original,
            "tiempo_restante": self.tiempo_restante,
            "prioridad": self.prioridad,
            "registros": self.registros,
            "memoria": self.memoria,
            "archivos_abiertos": self.archivos_abiertos,
            "usuario": self.usuario,
            "tiempo_inicio": self.tiempo_inicio,
            "tiempo_finalizacion": self.tiempo_finalizacion,
            "tiempo_espera": self.tiempo_espera,
            "tiempo_retorno": self.tiempo_retorno,
        }

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Actualizar campos del PCB a partir de un dict (útil al recibir JSON)."""
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def __repr__(self) -> str:
        return f"PCB(pid={self.pid}, estado={self.estado}, rafaga_cpu={self.rafaga_cpu})"
