import datetime
from config import mongo_db, sql_conn

# Colecciones NoSQL
productos_coll = mongo_db['productos']
carritos_coll = mongo_db['carritos']

# ==========================================
# 🛠️ OPERACIONES DEL CATÁLOGO (MongoDB NoSQL)
# ==========================================

def insertar_producto_nosql(sku, nombre, precio, stock, categoria, atributos):
    try:
        nuevo = {
            "sku": sku, "nombre": nombre, "precio": float(precio),
            "stock": int(stock), "categoria": categoria, "atributos": atributos
        }
        productos_coll.insert_one(nuevo)
        print(f"✅ Catálogo NoSQL Actualizado: {sku}")
    except Exception as e:
        print(f"❌ Error de Validación NoSQL: {e}")

def buscar_producto_nosql(sku):
    res = productos_coll.find_one({"sku": sku})
    print(f"🔍 Resultado en Catálogo NoSQL: {res}")
    return res

def agregar_al_carrito_nosql(usuario_id, sku, cantidad, precio):
    try:
        filtro = {"usuario_id": usuario_id, "estado": "activo"}
        item = {
            "sku": sku, "cantidad": int(cantidad),
            "precio_capturado": float(precio), "añadido_en": datetime.datetime.utcnow()
        }
        carritos_coll.update_one(
            filtro,
            {
                "$set": {"actualizado_en": datetime.datetime.utcnow()},
                "$push": {"items": item}
            },
            upsert=True
        )
        print(f"🛒 Item {sku} añadido al carrito NoSQL del usuario {usuario_id}.")
    except Exception as e:
        print(f"❌ Error al gestionar carrito NoSQL: {e}")

# ==========================================
# 🔄 FLUJO MAESTRO POLÍGLOTA: PROCESAR CHECKOUT
# ==========================================

def simular_pago_checkout(usuario_id, rut_cliente, nombre_cliente, email_facturacion, direccion_tributaria):
    """Une los dos mundos: Valida en MySQL, factura en MySQL y actualiza en MongoDB"""
    # 1. Obtener el carrito activo de MongoDB
    carrito = carritos_coll.find_one({"usuario_id": usuario_id, "estado": "activo"})
    if not carrito or not carrito.get("items"):
        print("⚠️ El carrito de compras NoSQL está vacío.")
        return

    cursor = sql_conn.cursor()
    try:
        # Iniciamos transacción ACID en MySQL
        sql_conn.start_transaction()

        # Asegurar o insertar el cliente contable en SQL
        cursor.execute(
            "INSERT IGNORE INTO clientes_financiero (rut_cliente, nombre_completo, email_facturacion, direccion_tributaria) VALUES (%s, %s, %s, %s)",
            (rut_cliente, nombre_cliente, email_facturacion, direccion_tributaria)
        )
        cursor.execute("SELECT id_cliente FROM clientes_financiero WHERE rut_cliente = %s", (rut_cliente,))
        id_cliente = cursor.fetchone()[0]

        monto_total = 0.0

        # Evaluar y descontar stock por cada ítem del carrito
        for item in carrito["items"]:
            sku = item["sku"]
            cant_comprar = item["cantidad"]
            precio_un = item["precio_capturado"]

            # Verificar Stock Crítico en MySQL
            cursor.execute("SELECT cantidad_bodega FROM inventario_critico WHERE sku = %s FOR UPDATE", (sku,))
            row = cursor.fetchone()
            if not row:
                raise Exception(f"El producto con SKU {sku} no está registrado en el inventario crítico SQL.")
            
            stock_actual = row[0]
            if stock_actual < cant_comprar:
                raise Exception(f"❌ Stock insuficiente en MySQL para {sku}. Disponible: {stock_actual}, Solicitado: {cant_comprar}")

            # Descontar stock crítico
            cursor.execute("UPDATE inventario_critico SET cantidad_bodega = cantidad_bodega - %s WHERE sku = %s", (cant_comprar, sku))
            monto_total += (precio_un * cant_comprar)

        # Crear Factura Contable en MySQL
        iva = monto_total * 0.19
        cursor.execute(
            "INSERT INTO facturas (id_cliente, monto_total, impuesto_iva, estado_pago) VALUES (%s, %s, %s, 'PAGADO')",
            (id_cliente, monto_total, iva)
        )
        
        # Si todo va bien en SQL, confirmamos cambios
        sql_conn.commit()
        print(f"💰 ¡Transacción Financiera ACID Exitosa! Factura creada por ${monto_total:.2f}.")

        # 2. Sincronizar el éxito contable con MongoDB (Vaciar carrito y cambiar estado)
        carritos_coll.update_one(
            {"usuario_id": usuario_id, "estado": "activo"},
            {"$set": {"estado": "convertido", "actualizado_en": datetime.datetime.utcnow()}}
        )
        print("🧹 Carrito NoSQL marcado como CONVERTIDO y vaciado con éxito.")

    except Exception as err:
        sql_conn.rollback()
        print(f"🚨 ROLLBACK EJECUTADO: Transacción cancelada por seguridad. Razón: {err}")
    finally:
        cursor.close()

# ==========================================
# 🎮 MENÚ INTERACTIVO EN VIVO (Bucle Infinito)
# ==========================================
if __name__ == "__main__":
    while True:
        print("\n===========================================")
        print("       SISTEMA POLÍGLOTA COMERCIOTECH      ")
        print("===========================================")
        print("1. Insertar producto en Catálogo NoSQL")
        print("2. Consultar producto por SKU (NoSQL)")
        print("3. Añadir producto al Carrito de Compras (NoSQL)")
        print("4. Procesar Pago y Generar Factura (Políglota SQL/NoSQL)")
        print("5. Salir")
        
        op = input("Seleccione una opción: ")

        if op == "1":
            sku = input("SKU: ")
            nom = input("Nombre: ")
            pr = input("Precio: ")
            st = input("Stock inicial: ")
            cat = input("Categoría: ")
            insertar_producto_nosql(sku, nom, pr, st, cat, {"origen": "Importado"})
        elif op == "2":
            sku = input("Ingrese SKU a buscar: ")
            buscar_producto_nosql(sku)
        elif op == "3":
            uid = input("ID de Usuario: ")
            sku = input("SKU del Producto: ")
            cant = input("Cantidad a comprar: ")
            pr = input("Precio pactado unitario: ")
            agregar_al_carrito_nosql(uid, sku, cant, pr)
        elif op == "4":
            uid = input("ID de Usuario para procesar: ")
            rut = input("RUT Facturación: ")
            nom = input("Nombre Razon Social: ")
            em = input("Email Facturación: ")
            dir_t = input("Dirección Tributaria: ")
            simular_pago_checkout(uid, rut, nom, em, dir_t)
        elif op == "5":
            print("Desconectando servicios...")
            break
        else:
            print("Opción inválida.")