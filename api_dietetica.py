from flask import Flask, jsonify, request, render_template
import sqlite3
import os

app = Flask(__name__)

# Se define la ruta absoluta para la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'dietetica.db')

def init_db():
    # Se verifica la existencia del archivo de base de datos
    print(f"-> Verificando base de datos en: {DB_NAME}")
    if not os.path.exists(DB_NAME):
        print("-> La base de datos no existe. Creando y poblando tablas...")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # Se crean las tablas de productos y carrito
        c.execute('''CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL, imagen TEXT)''')
        c.execute('''CREATE TABLE carrito (id INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER, FOREIGN KEY(producto_id) REFERENCES productos(id))''')
        
        productos = [
            (1, "Caja barra Laddubar", 31400, "productoA.webp"),
            (2, "Suplemento Nutri-Leva", 9900, "productoB.webp"),
            (3, "Barra de chocolate", 1500, "productoC.webp"),
            (4, "Edulcorante Pure Via", 27000, "productoD.webp"),
            (5, "Mermelada Equal", 3600, "productoE.webp"),
            (6, "Suplemento Brutal Mass", 54900, "productoF.webp"),
            (7, "Suplemento Satial Food", 38000, "productoG.webp"),
            (8, "Barra de frutos rojos", 1800, "productoH.webp"),
            (9, "Edulcorante Sucaryl", 4300, "productoI.webp")
        ]
        # Se inserta la lista de productos inicial
        c.executemany('INSERT INTO productos VALUES (?,?,?,?)', productos)
        conn.commit()
        conn.close()
        print("-> ¡Base de datos creada exitosamente!")
    else:
        print("-> La base de datos ya existía.")

# Se ejecuta la inicialización al arrancar
init_db()

def get_db_connection():
    # Se establece conexión con la base de datos
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # Se renderiza la página principal
    return render_template('index.html')

@app.route('/productos', methods=['GET'])
def get_productos():
    # Se obtiene la lista completa de productos
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return jsonify([dict(row) for row in productos])

@app.route('/carrito/<int:id_producto>', methods=['POST'])
def post_carrito(id_producto):
    # Se agrega un producto al carrito
    conn = get_db_connection()
    conn.execute('INSERT INTO carrito (producto_id) VALUES (?)', (id_producto,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Agregado al carrito'}), 200

@app.route('/carrito/<int:id_carrito>', methods=['DELETE'])
def delete_item(id_carrito):
    # Se elimina un producto del carrito
    conn = get_db_connection()
    conn.execute('DELETE FROM carrito WHERE id = ?', (id_carrito,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Eliminado'}), 200

@app.route('/carrito/total', methods=['GET'])
def get_total():
    # Se consulta el contenido total del carrito
    conn = get_db_connection()
    items = conn.execute('''
        SELECT c.id as id_carrito, p.nombre, p.precio 
        FROM carrito c JOIN productos p ON c.producto_id = p.id
    ''').fetchall()
    conn.close()
    
    lista_carrito = [dict(row) for row in items]
    # Se realiza la suma del precio total
    total = sum(item['precio'] for item in lista_carrito)
    
    return jsonify({'carrito': lista_carrito, 'total': total}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)