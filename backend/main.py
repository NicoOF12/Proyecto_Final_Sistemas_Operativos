from fastapi import FastAPI
from controllers.colas import router as colas_router

app = FastAPI(
    title="Simulador de Planificación de Procesos",
    description="Proyecto final: simulador con colas, cambios de contexto y algoritmos de planificación",
    version="1.0.0"
)

# --- Registrar rutas ---
app.include_router(colas_router)

@app.get("/")
def home():
    return {"mensaje": "Servidor FastAPI funcionando correctamente 🚀"}
