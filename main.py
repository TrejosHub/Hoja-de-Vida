from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contacto(BaseModel):
    nombre: str
    email: str
    mensaje: str

@app.post("/contacto")
def contacto(data: Contacto):
    url = f"{SUPABASE_URL}/rest/v1/contact_messages"

    payload = {
        "nombre": data.nombre,
        "email": data.email,
        "mensaje": data.mensaje,
        "fecha": datetime.now().isoformat()
    }

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    res = requests.post(url, json=payload, headers=headers)

    if res.status_code in (200, 201):
        return {"status": "ok", "msg": "Guardado en Supabase ✔️"}
    else:
        return {
            "status": "error",
            "detail": res.text
        }
