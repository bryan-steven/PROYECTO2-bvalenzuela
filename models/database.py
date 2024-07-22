from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Float, nullable=False)
    inventario = db.Column(db.Float, nullable=False)
    es_vegetariano = db.Column(db.Boolean, nullable=False)
    productos = db.relationship('ProductoIngrediente', back_populates='ingrediente', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    volumen = db.Column(db.Float, nullable=True)  # Volumen solo para Malteadas
    ingredientes = db.relationship('ProductoIngrediente', back_populates='producto', lazy=True)

class ProductoIngrediente(db.Model):
    __tablename__ = 'productos_ingredientes'
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
    cantidad = db.Column(db.Float, nullable=False)
    producto = db.relationship('Producto', back_populates='ingredientes', lazy=True)
    ingrediente = db.relationship('Ingrediente', back_populates='productos', lazy=True)
