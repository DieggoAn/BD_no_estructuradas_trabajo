import os
from pymongo import MongoClient

# En producción leerías esto con 'os.getenv' desde tu archivo .env
# Para tu prueba local/Docker, configuramos la cadena oficial con tus credenciales:
USER = "cybersec_admin"
PASS = "Mongo30"
HOST = "comerciotech_nosql"  # Cambiar por 'comerciotech_nosql' si metes Python dentro de Docker
PORT = "27017"
AUTH_DB = "admin"
DB_NAME = "comerciotech_catalogo"

# URI Corregida y estructurada de forma segura
MONGO_URI = f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}?authSource={AUTH_DB}"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    # Probamos la conexión
    client.server_info()
    print("🔒 Conexión segura establecida exitosamente con MongoDB.")
except Exception as e:
    print(f"❌ Error crítico de conexión: {e}")
    exit(1)