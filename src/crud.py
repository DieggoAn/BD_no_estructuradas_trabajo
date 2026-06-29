from config import db
from bson.objectid import ObjectId

# Apuntamos a tu colección real
collection = db['productos']

def insertar_producto(sku, nombre, precio, stock, categoria, atributos):
    """Inserta un producto respetando el esquema estricto de MongoDB"""
    try:
        nuevo_producto = {
            "sku": sku,
            "nombre": nombre,
            "precio": float(precio),       # Forzamos double
            "stock": int(stock),           # Forzamos int
            "categoria": categoria,
            "atributos": atributos         # Debe ser un objeto/diccionario
        }
        result = collection.insert_one(nuevo_producto)
        print(f"✅ Producto insertado con ID: {result.inserted_id}")
    except Exception as e:
        print(f"❌ Error de Validación (El esquema rechazó el documento): {e}")

def buscar_producto_por_sku(sku):
    """Busca un documento por su SKU único"""
    result = collection.find_one({"sku": sku})
    if result:
        print(f"🔍 Producto encontrado: {result}")
        return result
    print("⚠️ No se encontró ningún producto con ese SKU.")
    return None

def actualizar_precio_stock(sku, nuevo_precio, nuevo_stock):
    """Actualiza datos usando operadores nativos de MongoDB ($set)"""
    filtro = {"sku": sku}
    nuevos_valores = {
        "$set": {
            "precio": float(nuevo_precio),
            "stock": int(nuevo_stock)
        }
    }
    result = collection.update_one(filtro, nuevos_valores)
    print(f"🔄 Documentos modificados: {result.modified_count}")

def eliminar_producto_por_sku(sku):
    """Elimina un producto de forma definitiva"""
    result = collection.delete_one({"sku": sku})
    print(f"🗑️ Documentos eliminados: {result.deleted_count}")

# ==========================================
# 🧪 ÁREA DE PRUEBAS (Para demostrar en vivo)
# ==========================================
if __name__ == "__main__":
    print("\n--- Ejecutando pruebas del CRUD ---")
    
    # 1. Probar inserción válida
    insertar_producto(
        sku="CT-TECLADO-02",
        nombre="Teclado Mecánico RGB",
        precio=89.99,
        stock=25,
        categoria="Accesorios",
        atributos={"idioma": "Español", "switches": "Blue"}
    )
    
    # 2. Probar Búsqueda
    buscar_producto_por_sku("CT-TECLADO-02")
    
    # 3. Probar Actualización
    actualizar_precio_stock("CT-TECLADO-02", 79.99, 20)