from models.database import db, Producto, Ingrediente

class Heladeria:
    def __init__(self):
        self.productos = Producto.query.all()
        self.ingredientes = Ingrediente.query.all()

    def vender(self, producto_id, cantidad):
        producto = Producto.query.get(producto_id)
        if not producto:
            raise ValueError(f"Producto con ID {producto_id} no encontrado.")
        
        ingredientes = producto.ingredientes
        for ingrediente in ingredientes:
            if ingrediente.inventario < cantidad:
                raise ValueError(f"Ingrediente {ingrediente.nombre} no tiene suficiente inventario.")
        
        try:
            # Decrementar inventario
            for ingrediente in ingredientes:
                ingrediente.inventario -= cantidad
            
            # Realizar el commit de la transacción
            db.session.commit()
            return "¡Vendido!"
        
        except Exception as e:
            db.session.rollback()  # Revertir cambios en caso de error
            raise RuntimeError(f"Error al realizar la venta: {e}")