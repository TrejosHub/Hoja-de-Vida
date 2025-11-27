from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ------- CORS FIX --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # en producción cámbialo por tu dominio
    allow_credentials=True,
    allow_methods=["*"],       # <-- IMPORTANTE para OPTIONS
    allow_headers=["*"],
)
# -------------------------

class Contacto(BaseModel):
    nombre: str
    email: str
    mensaje: str

@app.post("/contacto")
def contacto(data: Contacto):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO contact_messages (nombre, email, mensaje, fecha)
        VALUES (%s, %s, %s, %s)
        """,
        (data.nombre, data.email, data.mensaje, datetime.now())
    )

    conn.commit()
    conn.close()

    return {"status": "ok", "msg": "Guardado correctamente"}