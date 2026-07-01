# Usamos una imagen oficial y liviana de Python
FROM python:3.11-slim

# Seteamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# SOLUCIÓN: Instalamos Netcat (nc) para que funcione el script de espera en el docker-compose
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Instalamos las librerías de MongoDB y MySQL
RUN pip install --no-cache-dir pymongo mysql-connector-python

# Copiamos todo el contenido de nuestra carpeta 'src' local dentro de '/app'
COPY src/ /app/

# Comando por defecto al encender el contenedor
CMD ["python", "crud.py"]