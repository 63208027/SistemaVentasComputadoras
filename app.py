from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from config import Config
from datetime import datetime

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Configurar la conexión a MySQL
mysql = MySQL(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelo de Usuario
class User(UserMixin):
    def __init__(self, id, email, rol):
        self.id = id
        self.email = email
        self.rol = rol

# Cargar el usuario por ID
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(id=user[0], email=user[2], rol=user[4])
    return None

# Ruta principal redirige a login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Ruta para registro de nuevos usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        hashed_password = generate_password_hash(contraseña, method='pbkdf2:sha256')
        rol = request.form['rol']
        
        # Inserta el nuevo usuario en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)", (nombre, email, hashed_password, rol))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('login'))
    return render_template('registro.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        # Verifica si el usuario existe
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[3], contraseña):
            user_obj = User(id=user[0], email=user[2], rol=user[4])
            login_user(user_obj)
            session['rol'] = user[4]
            if user[4] == 'administrador':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('cliente_dashboard'))
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('login.html')

# Ruta para agregar un producto
@app.route('/agregar_producto', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    if 'rol' not in session or session['rol'] != 'administrador':
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        imagen = request.form['imagen']
        
        # Inserta el nuevo producto en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Productos (nombre, descripcion, precio, cantidad, imagen) VALUES (%s, %s, %s, %s, %s)", (nombre, descripcion, precio, cantidad, imagen))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('admin_dashboard'))
    
    # Lista de imágenes en la carpeta static/images
    imagenes = os.listdir(os.path.join(app.static_folder, "images"))
    return render_template('agregar_producto.html', imagenes=imagenes)

# Ruta para modificar un producto
@app.route('/modificar_producto', methods=['GET', 'POST'])
@login_required
def modificar_producto():
    cursor = mysql.connection.cursor()
    
    productos = []

    if request.method == 'GET':
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        cursor.close()
        return render_template('modificar_producto.html', productos=productos)
    
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        
        if 'nombre' in request.form:  # Verificar si estamos en la fase de modificación
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio = request.form['precio']
            cantidad = request.form['cantidad']

            # Actualiza el producto en la base de datos
            cursor.execute("""
                UPDATE Productos 
                SET nombre = %s, descripcion = %s, precio = %s, cantidad = %s
                WHERE id_producto = %s
            """, (nombre, descripcion, precio, cantidad, id_producto))
            
            mysql.connection.commit()
            cursor.close()
            
            return redirect(url_for('admin_dashboard'))
        else:  # Si no, estamos en la fase de selección
            cursor.execute("SELECT * FROM Productos WHERE id_producto = %s", (id_producto,))
            producto = cursor.fetchone()
            cursor.close()
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM Productos")
            productos = cursor.fetchall()
            cursor.close()
            return render_template('modificar_producto.html', productos=productos, producto=producto)

#Ruta para marcar un producto agotado
@app.route('/marcar_agotado/<int:id_producto>', methods=['POST'])
@login_required
def marcar_agotado(id_producto):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Productos SET estado = 'agotado' WHERE id_producto = %s", (id_producto,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin_dashboard'))

# Ruta para ver los clientes
@app.route('/ver_clientes')
@login_required
def ver_clientes():
    if 'rol' not in session or session['rol'] != 'administrador':
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE rol = 'cliente'")
    clientes = cursor.fetchall()
    cursor.close()

    return render_template('ver_clientes.html', clientes=clientes)

# Ruta para el panel del cliente
@app.route('/cliente')
@login_required
def cliente_dashboard():
    return render_template('cliente_dashboard.html')

# Ruta para ver los productos
@app.route('/ver_productos')
@login_required
def ver_productos():
    categoria = request.args.get('categoria')
    print("CATEGORIA RECIBIDA:", categoria)

    cursor = mysql.connection.cursor()

    if categoria:
        cursor.execute(
            "SELECT * FROM Productos WHERE categoria = %s",
            (categoria,)
        )
    else:
        cursor.execute("SELECT * FROM Productos")

    productos = cursor.fetchall()
    cursor.close()

    # Obtener productos ya seleccionados del carrito
    carrito = session.get('carrito', [])
    carrito_productos = [item['id'] for item in carrito]

    return render_template(
        'ver_productos.html',
        productos=productos,
        carrito_productos=carrito_productos
    )

# Ruta para ver los pedidos del cliente
@app.route('/ver_pedidos')
@login_required
def ver_pedidos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Pedidos WHERE id_usuario = %s", (current_user.id,))
    pedidos = cursor.fetchall()
    cursor.close()
    return render_template('ver_pedidos.html', pedidos=pedidos)


# Ruta para agregar productos seleccionados al carrito
@app.route('/agregar_seleccionados_al_carrito', methods=['POST'])
@login_required
def agregar_seleccionados_al_carrito():

    productos_seleccionados = request.form.getlist('productos')
    carrito = session.get('carrito', [])

    cursor = mysql.connection.cursor()

    for id_producto in productos_seleccionados:

        precio = float(request.form[f'precio_{id_producto}'])
        cantidad = int(request.form.get(f'cantidad_{id_producto}', 1))

        # Obtener datos del producto
        cursor.execute(
            "SELECT nombre, descripcion FROM Productos WHERE id_producto = %s",
            (id_producto,)
        )
        producto = cursor.fetchone()

        nombre = producto[0]
        descripcion = producto[1]

        # Verificar si ya existe en el carrito
        existe = False

        for item in carrito:
            if item['id'] == int(id_producto):
                item['cantidad'] += 1
                existe = True
                break

        if not existe:
            carrito.append({
                'id': int(id_producto),
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'cantidad': cantidad
            })

    cursor.close()

    session['carrito'] = carrito

    return redirect(url_for('ver_carrito'))
# Ruta para ver el carrito de compras
@app.route('/ver_carrito')
@login_required
def ver_carrito():

    carrito = session.get('carrito', [])

    mostrar_pago = request.args.get('pago', '0')

    return render_template(
        'ver_carrito.html',
        carrito=carrito,
        mostrar_pago=mostrar_pago
    )

# Ruta para crear un pedido
@app.route('/crear_pedido', methods=['POST'])
@login_required
def crear_pedido():
    productos_seleccionados = request.form.getlist('productos')
    if not productos_seleccionados:
        return redirect(url_for('ver_productos'))

    # Crear un nuevo pedido
    fecha_pedido = datetime.now()
    estado = 'pendiente'
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Pedidos (id_usuario, fecha_pedido, estado) VALUES (%s, %s, %s)", (current_user.id, fecha_pedido, estado))
    id_pedido = cursor.lastrowid

    # Añadir detalles del pedido
    for id_producto in productos_seleccionados:
        precio_unitario = float(request.form[f'precio_{id_producto}'])
        cantidad = int(request.form.get(f'cantidad_{id_producto}', 1))
        total = cantidad * precio_unitario
        cursor.execute("INSERT INTO DetallePedidos (id_pedido, id_producto, cantidad, precio_unitario, total) VALUES (%s, %s, %s, %s, %s)", 
                       (id_pedido, id_producto, cantidad, precio_unitario, total))
        
        # Actualizar la cantidad del producto en la tabla Productos
        cursor.execute("UPDATE Productos SET cantidad = cantidad - %s WHERE id_producto = %s", (cantidad, id_producto))
    
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('pagar', id_pedido=id_pedido))

# Ruta para proceder con el pago
@app.route('/pagar/<int:id_pedido>')
@login_required
def pagar(id_pedido):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM DetallePedidos WHERE id_pedido = %s", (id_pedido,))
    detalles_pedido = cursor.fetchall()
    cursor.close()
    return render_template('pagar.html', detalles_pedido=detalles_pedido, id_pedido=id_pedido)

# Ruta para completar el pago
@app.route('/completar_pago/<int:id_pedido>', methods=['POST'])
@login_required
def completar_pago(id_pedido):
    cursor = mysql.connection.cursor()
    
    # Actualizar el estado del pedido a 'completado'
    cursor.execute("UPDATE Pedidos SET estado = 'completado' WHERE id_pedido = %s", (id_pedido,))
    mysql.connection.commit()
    cursor.close()

    # Vaciar carrito después del pago
    session['carrito'] = []
    
    return redirect(url_for('pago_completado'))

# Ruta para mostrar el mensaje de pago completado
@app.route('/pago_completado')
@login_required
def pago_completado():
    return '''
    <div style="text-align:center; margin-top:100px;">
        <h1>Pago completo, su pedido se está enviando</h1>

        <br><br>

        <a href="/cliente"
           style="
           background-color:#6c757d;
           color:white;
           padding:10px 20px;
           text-decoration:none;
           border-radius:5px;">
           Volver al Menú Principal
        </a>
    </div>
    '''
    # Ruta para eliminar del carito el producto seleccionado
@app.route('/eliminar_del_carrito/<int:id_producto>')
@login_required
def eliminar_del_carrito(id_producto):

    carrito = session.get('carrito', [])

    carrito = [item for item in carrito if item['id'] != id_producto]

    session['carrito'] = carrito

    return redirect(url_for('ver_carrito'))

# Ruta para el panel del administrador
@app.route('/admin')
@login_required
def admin_dashboard():
    if 'rol' in session and session['rol'] == 'administrador':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        cursor.close()
        return render_template('admin_dashboard.html', productos=productos)
    return redirect(url_for('login'))

# Ruta para eliminar un producto
@app.route('/eliminar_producto/<int:id_producto>', methods=['POST'])
@login_required
def eliminar_producto(id_producto):
    if 'rol' not in session or session['rol'] != 'administrador':
        return redirect(url_for('login'))

    # Elimina el producto de la base de datos
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Productos WHERE id_producto = %s", (id_producto,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin_dashboard'))

# Ruta para cambiar el estado de un producto (disponible/agotado)
@app.route('/cambiar_estado_producto/<int:id_producto>', methods=['POST'])
@login_required
def cambiar_estado_producto(id_producto):
    if 'rol' not in session or session['rol'] != 'administrador':
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT estado FROM Productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    nuevo_estado = 'disponible' if producto[0] == 'agotado' else 'agotado'
    
    # Actualiza el estado del producto en la base de datos
    cursor.execute("UPDATE Productos SET estado = %s WHERE id_producto = %s", (nuevo_estado, id_producto))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin_dashboard'))

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
