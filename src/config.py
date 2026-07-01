import os
from pymongo import MongoClient
import mysql.connector

# --- CONFIGURACIÓN MONGODB ---
MONGO_USER = "srv_app_comerciotech"  # Usamos el usuario con privilegio mínimo de tu RBAC
MONGO_PASS = "Python1!"
MONGO_HOST = "comerciotech_nosql"
MONGO_PORT = "27017"
MONGO_DB = "comerciotech_catalogo"

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource={MONGO_DB}"

# --- CONFIGURACIÓN MYSQL ---
SQL_USER = "srv_app_sql"
SQL_PASS = "AppSqlPass2026*"
SQL_HOST = "comerciotech_sql"
SQL_DB = "comerciotech_financiero"

# Conexión a MongoDB
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_db = mongo_client[MONGO_DB]
    mongo_client.server_info()
    print("🔒 Conexión segura establecida exitosamente con MongoDB NoSQL.")
except Exception as e:
    print(f"❌ Error crítico en MongoDB: {e}")
    exit(1)

# Conexión a MySQL
try:
    sql_conn = mysql.connector.connect(
        host=SQL_HOST,
        user=SQL_USER,
        password=SQL_PASS,
        database=SQL_DB
    )
    print("🔒 Conexión segura establecida exitosamente con MySQL SQL.")
except Exception as e:
    print(f"❌ Error crítico en MySQL: {e}")
    exit(1)