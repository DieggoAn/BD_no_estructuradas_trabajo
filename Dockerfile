# Usamos una imagen oficial y liviana de Python
FROM python:3.11-slim

# Seteamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalamos la librería de MongoDB
RUN pip install --no-cache-dir pymongo

# Copiamos todo el contenido de nuestra carpeta 'src' local dentro de '/app'
COPY src/ /app/

# Comando por defecto al encender el contenedor (ejecutar nuestro CRUD)
CMD ["python", "crud.py"]