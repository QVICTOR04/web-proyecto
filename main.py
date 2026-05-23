from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc

app = FastAPI()

# Configuración de CORS para que tu HTML (Live Server) pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambia esto por tu dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cadena de conexión a tu SQL Server (Ajusta tus datos aquí)
CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=192.168.1.247;"
    "DATABASE=matriz;"
    "UID=60754592;"
    "PWD=2004;trustservercertificate=yes;"
)

# Modelo de datos para validar lo que envías desde el HTML
class Usuario(BaseModel):
    DNI: str
    email: str

# 1. READ (Obtener todos los usuarios)
@app.get("/api/usuarios")
def obtener_usuarios():
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("SELECT RECLUTADOR,[FUENTE DE RECLUTAMIENTO],PUESTO,NOMBRES"
                       ",APELLIDOS,DNI,CELULAR,DISTRITO,[ESTADO DEL PROCESO] FROM matriz.dbo.reclutamiento")
        
        usuarios = []
        for row in cursor.fetchall():
            usuarios.append({"id": row[0], "DNI": row[1], "email": row[2]})
            
        conn.close()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. CREATE (Insertar un usuario)
@app.post("/api/usuarios")
def crear_usuario(usuario: Usuario):
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reclutamiento (DNI, email) VALUES (?, ?)",
            (usuario.DNI, usuario.email)
        )
        conn.commit()
        conn.close()
        return {"message": "Usuario creado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. DELETE (Eliminar un usuario)
@app.delete("/api/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reclutamiento WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()
        return {"message": "Usuario eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))