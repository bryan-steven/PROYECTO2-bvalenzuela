from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from controllers.heladeria_controller import get_productos, calcular_calorias, get_ingredientes, es_sano, producto_mas_rentable
import os
from models.database import db, Producto, Ingrediente
from models.heladeria import Heladeria

load_dotenv()
secret_key = os.urandom(24)

app = Flask(__name__)
app.secret_key = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}/{os.getenv("SCHEMA_DB")}'
app.config["SECRET_KEY"] = secret_key
db.init_app(app)

@app.route('/')
def index():
    return 'Bienvenido a la Heladeria'

@app.route('/productos')
def productos():
    productos = get_productos()
    return render_template('productos.html', productos=productos)

@app.route('/ingredientes')
def ingredientes():
    ingredientes = get_ingredientes()
    return render_template('ingredientes.html', ingredientes=ingredientes)

@app.route('/calorias')
def mostrar_calorias():
    resultados = calcular_calorias()
    return render_template('calorias.html', resultados=resultados)

@app.route('/sano')
def mostrar_sano():
    resultados = es_sano()
    return render_template('sanidad.html', resultados=resultados)

@app.route('/rentabilidad')
def rentabilidad():
    productos = Producto.query.all()
    return render_template('rentabilidad.html', productos=productos)

@app.route('/abastecer_inventario')
def mostrar_abastecer_inventario():
    ingredientes = Ingrediente.query.all()
    return render_template('abastecer_inventario.html', ingredientes=ingredientes)

@app.route('/abastecer/<int:ingrediente_id>', methods=['POST'])
def abastecer(ingrediente_id):
    cantidad = request.form['cantidad']
    try:
        cantidad = float(cantidad)
        ingrediente = Ingrediente.query.get(ingrediente_id)
        if ingrediente:
            ingrediente.abastecer_inventario(cantidad)
            flash(f'Se ha abastecido {cantidad} unidades de {ingrediente.nombre}.')
        else:
            flash('Ingrediente no encontrado.')
    except ValueError:
        flash('Cantidad inválida.')
    except Exception as e:
        flash(str(e))
    
    return redirect(url_for('mostrar_abastecer_inventario'))

@app.route('/renovar_inventario')
def mostrar_renovar_inventario():
    ingredientes = Ingrediente.query.all()
    return render_template('renovar_inventario.html', ingredientes=ingredientes)

@app.route('/renovar/<int:ingrediente_id>', methods=['POST'])
def renovar(ingrediente_id):
    ingrediente = Ingrediente.query.get(ingrediente_id)
    if ingrediente:
        try:
            ingrediente.renovar_inventario()
            flash(f'Se ha renovado el inventario de {ingrediente.nombre}.')
        except Exception as e:
            flash(str(e))
    else:
        flash('Ingrediente no encontrado.')
    
    return redirect(url_for('mostrar_renovar_inventario'))

@app.route('/costo_produccion')
def mostrar_costo_produccion():
    productos = Producto.query.all()
    return render_template('costo_produccion.html', productos=productos)

@app.route('/producto_mas_rentable')
def mostrar_producto_mas_rentable():
    producto = producto_mas_rentable()
    return render_template('producto_mas_rentable.html', producto=producto)

@app.route('/venta')
def mostrar_productos():
    heladeria = Heladeria()
    productos = heladeria.productos
    for producto in productos:
        print(f"ID: {producto.id}, Nombre: {producto.nombre}, Precio: {producto.precio_publico}")
    return render_template('productos_2.html', productos=productos)

@app.route('/vender', methods=['POST'])
def vender_producto():
    producto_id = request.form.get('producto_id')
    cantidad = int(request.form.get('cantidad'))
    
    heladeria = Heladeria()
    
    try:
        resultado = heladeria.vender(producto_id, cantidad)
        return render_template('resultado.html', mensaje=resultado)
    
    except ValueError as e:
        mensaje_error = str(e)
        ingrediente_faltante = mensaje_error.split(' ')[1]  # Ajusta esto según la estructura del mensaje de error
        return render_template('resultado.html', mensaje=f"¡Oh no! Nos hemos quedado sin {ingrediente_faltante}")
    
    except RuntimeError as e:
        return render_template('resultado.html', mensaje=f"Error al realizar la venta: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
