from fastapi import FastAPI
from controllers.colas import router as colas_router
from controllers.colas import cola_listos
from controllers.planificador import Planificador
from models.process import Proceso
from controllers.filesystem import router as filesystem_router

app = FastAPI(
    title="Simulador de Planificación de Procesos",
    description="Proyecto final: simulador con colas, cambios de contexto y algoritmos de planificación",
    version="1.0.0"
)

# --- Registrar rutas ---
app.include_router(colas_router)


app.include_router(filesystem_router)

@app.get("/")
def home():
    return {"mensaje": "Servidor FastAPI funcionando correctamente 🚀"}

lista_procesos = list(cola_listos.queue)

planificador = Planificador()

@app.post("/planificar/{algoritmo}")
def planificar(algoritmo: str):
    # copiamos los procesos de la cola como lista
    procesos = list(cola_listos.queue)

    for p in procesos:
        p.reset()

    if len(procesos) == 0:
        return {"error": "No hay procesos para planificar"}

    if algoritmo == "fcfs":
        return planificador.fcfs(procesos)
    elif algoritmo == "rr":
        return planificador.round_robin(procesos, quantum=2)
    elif algoritmo == "sjf":
        return planificador.sjf(procesos)
    else:
        return {"error": "Algoritmo no válido"}

