from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from controllers.heladeria_controller import get_productos, vender_producto
import os
from models.database import db

load_dotenv()
secret_key = os.urandom(24)

app = Flask(__name__)
app.secret_key = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}/{os.getenv("SCHEMA_DB")}'
app.config["SECRET_KEY"] = secret_key
db.init_app(app)

@app.route('/')
def index():
    productos = get_productos()
    return render_template('index.html', productos=productos)

@app.route('/vender/<nombre_producto>')
def vender(nombre_producto):
    mensaje = vender_producto(nombre_producto)
    return mensaje

if __name__ == '__main__':
    app.run(debug=True)
