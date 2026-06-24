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

print("🔒 ¡Entorno de base de datos inicializado y blindado correctamente!");