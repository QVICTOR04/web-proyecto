from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc
import os

app = FastAPI()

# Configuración de CORS para que tu HTML (Live Server) pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambia esto por tu dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cadena de conexión a tu SQL Server
# Intentar usar credenciales del .env o hardcodeadas
try:
    # Leer del archivo .env si existe
    BD_SERVER = os.getenv('bd_server', '192.168.1.247')
    BD_USER = os.getenv('bd_user', '60754592')
    BD_PASSWORD = os.getenv('bd_password', '2004')
    BD_DATABASE = os.getenv('db_database', 'matriz')
except:
    BD_SERVER = '192.168.1.247'
    BD_USER = '60754592'
    BD_PASSWORD = '2004'
    BD_DATABASE = 'matriz'

CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={BD_SERVER};"
    f"DATABASE={BD_DATABASE};"
    f"UID={BD_USER};"
    f"PWD={BD_PASSWORD};trustservercertificate=yes;"
)

print(f"Intentando conectar a: {BD_SERVER} - DB: {BD_DATABASE}")

# Modelo de datos para validar lo que envía el HTML
class Usuario(BaseModel):
    RECLUTADOR: str
    DNI: str

# 1. READ (Obtener todos los usuarios)
@app.get("/api/usuarios")
def obtener_usuarios():
    try:
        print("Conectando a la BD...")
        conn = pyodbc.connect(CONN_STR)
        print("Conexión exitosa!")
        cursor = conn.cursor()
        cursor.execute("SELECT top 10 id,RECLUTADOR,[FUENTE DE RECLUTAMIENTO],PUESTO,NOMBRES"
                       ",APELLIDOS,DNI,CELULAR,DISTRITO,[ESTADO DEL PROCESO] FROM matriz.dbo.reclutamiento ORDER BY id DESC")
        
        usuarios = []
        for row in cursor.fetchall():
            usuarios.append({"id": row[0], "RECLUTADOR": row[1], "FUENTE DE RECLUTAMIENTO": row[2]
                             , "PUESTO": row[3], "NOMBRES": row[4], "APELLIDOS": row[5], "DNI": row[6], "CELULAR": row[7]
                             , "DISTRITO": row[8], "ESTADO DEL PROCESO": row[9]})
            
        conn.close()
        return usuarios
    except Exception as e:
        print(f"Error en obtener_usuarios: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de BD: {str(e)}")

# 2. CREATE (Insertar un usuario)
@app.post("/api/usuarios")
def crear_usuario(usuario: Usuario):
    try:
        print(f"Insertando usuario: {usuario.RECLUTADOR} / {usuario.DNI}")
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO matriz.dbo.reclutamiento (RECLUTADOR, FUENTE DE RECLUTAMIENTO) VALUES (?, ?)",
            (usuario.RECLUTADOR, usuario["FUENTE DE RECLUTAMIENTO"])
        )
        conn.commit()
        conn.close()
        return {"message": "Usuario creado con éxito"}
    except Exception as e:
        print(f"Error en crear_usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar: {e}")
    
# 3. update (Actualizar un usuario)
@app.put("/api/usuarios")
def actualizar_usuario(usuario: Usuario):
    try:
        print(f"Actualizando usuario: {usuario.RECLUTADOR} / {usuario.DNI}")
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute
        "UPDATE matriz.dbo.reclutamiento SET RECLUTADOR = ?, FUENTE DE RECLUTAMIENTO = ?, CON / SIN EXPERIENCIA = ?, PUESTO = ?, NOMBRES = ?, APELLIDOS = ?, DNI / CE = ?,DNI = ?, CELULAR = ?, EDAD = ?,DISTRITO = ?, ESTADO DEL PROCESO = ?,FECHA DE CITA = ?,HORA DE CITA = ? ,ASISTIÓ SI / NO = ?,PASO ENTREVISTA = ?,MOTIVO = ?, OBSERVACIONES = ?,FECHA INICIO DE CAPA = ?"
        ",FECHA FIN DE CAPA = ?, asistió si / no.1	= ?,asistió (2)=?,	asistió (3)=?,	obsevaciones=?,	estado de capacitación=?,	asistió a su 1er día de gestión si / no=?,	se contrato	fecha de contrato=?,	carteras=?,	detalles = ? WHERE ID = ?",
        (usuario.RECLUTADOR, usuario["FUENTE DE RECLUTAMIENTO"], usuario["CON / SIN EXPERIENCIA"], usuario.PUESTO, usuario.NOMBRES, usuario.APELLIDOS, usuario.DNI, usuario.CELULAR, usuario.DISTRITO, usuario["ESTADO DEL PROCESO"], usuario["FECHA DE CITA"], usuario["HORA DE CITA"], usuario["ASISTIÓ SI / NO"], usuario["PASO ENTREVISTA"], usuario["MOTIVO"], usuario["OBSERVACIONES"]
        ,usuario["FECHA INICIO DE CAPA"], usuario["FECHA FIN DE CAPA"], usuario["asistió si / no.1"], usuario["asistió (2)"], usuario["asistió (3)"], usuario["obsevaciones"], usuario["estado de capacitación"], usuario["asistió a su 1er día de gestión si / no?"], usuario["fecha de contrato"], usuario["carteras"], usuario["detalles"], usuario.id)
        conn.commit()
        conn.close()
        return {"message": "Usuario actualizado con éxito"}
    except Exception as e:
        print(f"Error en actualizar_usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {e}")

# 4. DELETE (Eliminar un usuario)
@app.delete("/api/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    try:
        print(f"Eliminando usuario: {usuario_id}")
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM matriz.dbo.reclutamiento WHERE ID = ?", (usuario_id,))
        conn.commit()
        conn.close()
        return {"message": "Usuario eliminado"}
    except Exception as e:
        print(f"Error en eliminar_usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
