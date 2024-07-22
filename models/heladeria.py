from sqlalchemy.orm import Session
from models.database import db, Ingrediente, Producto, ProductoIngrediente

class Heladeria:
    
    def __init__(self, session: Session):
        self.session = session

    def calcular_calorias(self, producto_id):
        producto = self.session.get(Producto, producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        calorias_totales = 0
        for pi in producto.ingredientes:
            ingrediente = self.session.get(Ingrediente, pi.ingrediente_id)
            calorias_totales += ingrediente.calorias * pi.cantidad
        return calorias_totales

    def calcular_costo_produccion(self, producto_id):
        producto = self.session.get(Producto, producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        costo_total = 0
        for pi in producto.ingredientes:
            ingrediente = self.session.get(Ingrediente, pi.ingrediente_id)
            costo_total += ingrediente.precio * pi.cantidad
        return costo_total

    def calcular_rentabilidad(self, producto_id):
        producto = self.session.get(Producto, producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        costo = self.calcular_costo_produccion(producto_id)
        return producto.precio_publico - costo

    def renovar_inventario(self, ingrediente_id, cantidad):
        ingrediente = self.session.get(Ingrediente, ingrediente_id)
        if not ingrediente:
            raise ValueError("Ingrediente no encontrado")
        ingrediente.inventario += cantidad
        self.session.commit()

    def producto_mas_rentable(self):
        productos = self.session.query(Producto).all()
        mejor_producto = None
        max_rentabilidad = float('-inf')
        for producto in productos:
            rentabilidad = self.calcular_rentabilidad(producto.id)
            if rentabilidad > max_rentabilidad:
                max_rentabilidad = rentabilidad
                mejor_producto = producto
        return mejor_producto

    def vender(self, producto_id):
        producto = self.session.get(Producto, producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        for pi in producto.ingredientes:
            ingrediente = self.session.get(Ingrediente, pi.ingrediente_id)
            if ingrediente.inventario < pi.cantidad:
                raise ValueError("Inventario insuficiente para el ingrediente: " + ingrediente.nombre)
            ingrediente.inventario -= pi.cantidad
        self.session.commit()
