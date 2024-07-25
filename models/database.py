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
    #productos = db.relationship('productos', secondary='productos_ingredientes', lazy='subquery', backref=db.backref('ingredientes', lazy=True))
    
    def es_sano(self):
        if self.calorias < 100 or self.es_vegetariano:
            return "Es sano"
        else:
            "No es sano"

    def abastecer_inventario(self, cantidad):
        if cantidad > 0:
            self.inventario += cantidad
            db.session.commit()
        else:
            raise ValueError("La cantidad debe ser positiva")
    
    def renovar_inventario(self):
        self.inventario = 0
        db.session.commit()
        
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    volumen = db.Column(db.Float, nullable=True)
    ingredientes = db.relationship('Ingrediente', secondary='productos_ingredientes', lazy='subquery', backref=db.backref('productos', lazy=True))
    
    def calcular_calorias(self):
        sumatoria = 0
        for ingredientes in self.ingredientes:
            sumatoria += ingredientes.calorias
        return sumatoria * 0.95

    def calcular_costo(self):
        costo_total = 0
        for ingrediente in self.ingredientes:
            costo_total += ingrediente.precio
        return costo_total
    
    def calcular_rentabilidad(self):
        costo = self.calcular_costo()
        return self.precio_publico - costo
    
    def calcular_costo_produccion(self):
        return self.calcular_costo()

class ProductoIngrediente(db.Model):
    __tablename__ = 'productos_ingredientes'
    ingrediente_id = db.Column(db.Integer, db.ForeignKey("ingredientes.id"), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)