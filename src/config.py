import os
import time  # <-- AGREGADO
from pymongo import MongoClient
import mysql.connector

# --- CONFIGURACIÓN MONGODB ---
MONGO_USER = "cybersec_admin"        # 🚀 CORREGIDO
MONGO_PASS = "Mongo30"               # 🚀 CORREGIDO
MONGO_HOST = "comerciotech_nosql"
MONGO_PORT = "27017"
MONGO_DB = "admin"                   # 🚀 CORREGIDO (Apuntamos a la BD raíz)

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

# --- CONFIGURACIÓN MYSQL ---
SQL_USER = "srv_app_sql"
SQL_PASS = "AppSqlPass2026*"
SQL_HOST = "comerciotech_sql"
SQL_DB = "comerciotech_financiero"   # 🚀 Ya existe adentro

# Conexión Segura con Reintentos a MongoDB
print("⏳ Esperando inicialización segura de MongoDB...")
while True:
    try:
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        mongo_db = mongo_client[MONGO_DB]
        mongo_client.server_info()
        print("🔒 Conexión segura establecida exitosamente con MongoDB NoSQL.")
        break
    except Exception:
        print("... MongoDB inicializando. Reintentando en 2 segundos ...")
        time.sleep(2)

# Conexión Segura con Reintentos a MySQL
print("⏳ Esperando inicialización segura de MySQL...")
while True:
    try:
        sql_conn = mysql.connector.connect(
            host=SQL_HOST,
            user=SQL_USER,
            password=SQL_PASS,
            database=SQL_DB
        )
        print("🔒 Conexión segura establecida exitosamente con MySQL SQL.")
        break
    except Exception:
        print("... MySQL inicializando. Reintentando en 2 segundos ...")
        time.sleep(2)