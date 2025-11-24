from fastapi import APIRouter, HTTPException
from models.process import Proceso
from queue import Queue
from typing import List, Dict, Any

router = APIRouter(prefix="/colas", tags=["Colas"])

# --- Colas simuladas ---
cola_listos: Queue[Proceso] = Queue()
cola_bloqueados: Queue[Proceso] = Queue()

# --- Datos de prueba ---
procesos_test1 = [
    {"PID": 1, "tiempo_llegada": 0, "rafaga_cpu": 5, "usuario": "usuario1"},
    {"PID": 2, "tiempo_llegada": 0, "rafaga_cpu": 1, "usuario": "usuario2"},
]

def transformar_y_encolar(proceso_dict: Dict[str, Any]) -> Proceso:
    """Convierte un diccionario en una instancia de Proceso y la agrega a la cola de listos."""
    p = Proceso(
        pid=proceso_dict["PID"],
        estado="LISTO",
        tiempo_llegada=proceso_dict["tiempo_llegada"],
        rafaga_cpu=proceso_dict["rafaga_cpu"],
        prioridad=1,
        registros=[],
        memoria=None,
        archivos_abiertos=[],
        usuario=proceso_dict["usuario"]
    )

    p.cambiar_estado("Listo")
    cola_listos.put(p)
    return p


# Inicializamos los procesos de prueba
for pd in procesos_test1:
    transformar_y_encolar(pd)


# --- Rutas de API ---

@router.get("/procesos")
def listar_procesos() -> List[Dict[str, Any]]:
    """Lista todos los procesos en colas de listos y bloqueados."""
    salida = []
    for proc in list(cola_listos.queue):
        salida.append({
            "PID": proc.pcb.pid,
            "Estado": proc.pcb.estado
        })
    for proc in list(cola_bloqueados.queue):
        salida.append({
            "PID": proc.pcb.pid,
            "Estado": proc.pcb.estado
        })
    return salida


@router.post("/agregar")
def agregar_proceso(proceso: Dict[str, Any]) -> Dict[str, Any]:
    """Agrega un nuevo proceso a la cola de listos."""
    if not (
        "pid" in proceso or "PID" in proceso
    ) or not (
        "tiempo_llegada" in proceso or "tiempoLlegada" in proceso
    ) or not (
        "rafaga_cpu" in proceso or "rafaga_CPU" in proceso
    ) or not (
        "usuario" in proceso
    ):
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios del proceso")
    p = transformar_y_encolar(proceso)
    return {"PID": p.pcb.pid, "Estado": p.pcb.estado, "Tiempo Llegada": p.pcb.tiempo_llegada, "Ráfaga CPU": p.pcb.rafaga_cpu}


@router.post("/bloquear")
def bloquear_proceso() -> Dict[str, Any]:
    """Mueve el primer proceso de listos a bloqueados."""
    if cola_listos.empty():
        raise HTTPException(status_code=400, detail="No hay procesos en la cola de listos")
    p = cola_listos.get()
    p.pcb.estado = "BLOQUEADO"
    cola_bloqueados.put(p)
    return {"PID": p.pcb.pid, "Nuevo Estado": p.pcb.estado}


@router.post("/desbloquear")
def desbloquear_proceso() -> Dict[str, Any]:
    """Mueve el primer proceso de bloqueados a listos."""
    if cola_bloqueados.empty():
        raise HTTPException(status_code=400, detail="No hay procesos bloqueados")
    p = cola_bloqueados.get()
    p.pcb.estado = "LISTO"
    cola_listos.put(p)
    return {"PID": p.pcb.pid, "Nuevo Estado": p.pcb.estado}


@router.get("/mostrar")
def mostrar_colas() -> Dict[str, List[int]]:
    """Devuelve los PID de cada cola."""
    listos_pids = [proc.pcb.pid for proc in list(cola_listos.queue)]
    bloqueados_pids = [proc.pcb.pid for proc in list(cola_bloqueados.queue)]
    return {
        "cola_listos": listos_pids,
        "cola_bloqueados": bloqueados_pids
    }
