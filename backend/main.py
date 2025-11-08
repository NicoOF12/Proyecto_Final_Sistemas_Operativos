from fastapi import FastAPI

# Crear la aplicación FastAPI
app = FastAPI()

# Endpoint raíz
@app.get("/")
def home():
    return {"mensaje": "Servidor FastAPI funcionando correctamente 🚀"}

# Puedes agregar más rutas luego (procesos, planificadores, etc.)
