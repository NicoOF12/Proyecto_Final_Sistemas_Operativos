from fastapi import FastAPI
from models.process import Proceso

app = FastAPI()

# Lista simulada de procesos Caso 1: Procesos básicos
procesos_test1 = [
    {"PID": 1, "tiempo_llegada": 0, "rafaga_CPU": 5, "usuario": "usuario1"},
    {"PID": 1, "tiempo_llegada": 0, "rafaga_CPU": 5, "usuario": "usuario2"},
    # Proceso(1, prioridad=2, rafaga_cpu=5, tiempo_llegada=0),
    # Proceso(2, prioridad=1, rafaga_cpu=3, tiempo_llegada=2),
    # Proceso(3, prioridad=3, rafaga_cpu=7, tiempo_llegada=4),
]

@app.get("/")
def home():
    return {"mensaje": "Servidor FastAPI funcionando correctamente 🚀"}

@app.get("/procesos")
def listar_procesos():
    salida = []
    for p in procesos_test1:
        if isinstance(p, dict):
            salida.append(p)
        else:
            salida.append(p.pcb.to_dict())
    return salida
