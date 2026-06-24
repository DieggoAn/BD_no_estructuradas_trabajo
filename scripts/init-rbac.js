// Cambiar a la base de datos del proyecto
use comerciotech_catalogo;

// Crear el usuario con privilegio mínimo para la aplicación de Python
db.createUser({
  user: "srv_app_comerciotech",
  pwd: "Python1!",
  roles: [
    { role: "readWrite", db: "comerciotech_catalogo" }
  ]
});

// Crear la colección de productos con validación estricta de tipos de datos
db.createCollection("productos", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: [ "sku", "nombre", "precio", "stock", "categoria", "atributos" ],
         properties: {
            sku: { bsonType: "string" },
            nombre: { bsonType: "string" },
            precio: { bsonType: "double", minimum: 0.0 },
            stock: { bsonType: "int", minimum: 0 },
            categoria: { bsonType: "string" },
            atributos: { bsonType: "object" }
         }
      }
   }
});

// Crear índices de alto rendimiento para búsquedas inferiores a 50ms
db.productos.createIndex({ sku: 1 }, { unique: true });
db.productos.createIndex({ categoria: 1, precio: 1 });

//Carrito

db.createCollection("carritos", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: [ "usuario_id", "estado", "items", "actualizado_en" ],
         properties: {
            usuario_id: { bsonType: "string" },
            estado: { bsonType: "string", enum: [ "activo", "abandonado", "convertido" ] },
            actualizado_en: { bsonType: "date" },
            items: {
               bsonType: "array",
               items: {
                  bsonType: "object",
                  required: [ "sku", "cantidad", "precio_capturado", "añadido_en" ],
                  properties: {
                     sku: { bsonType: "string" },
                     cantidad: { bsonType: "int", minimum: 1 },
                     precio_capturado: { bsonType: "double", minimum: 0.0 },
                     añadido_en: { bsonType: "date" }
                  }
               }
            }
         }
      }
   }
});

// Crear índices de alto rendimiento para el carrito
db.carritos.createIndex({ usuario_id: 1, estado: 1 }, { unique: true });
db.carritos.createIndex({ actualizado_en: 1 }, { expireAfterSeconds: 1209600 });

print("🔒 ¡Entorno de base de datos inicializado y blindado correctamente!");
