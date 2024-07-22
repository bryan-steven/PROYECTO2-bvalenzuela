from models.database import db, Producto, ProductoIngrediente, Ingrediente

def get_productos():
    productos = Producto.query.all()  # Obtiene todos los productos de la base de datos
    return productos

def vender_producto(nombre_producto):
    """Vende un producto si existe en la base de datos y hay suficiente inventario."""
    # Buscar el producto por nombre
    producto = Producto.query.filter_by(nombre=nombre_producto).first()
    
    if not producto:
        return f'Producto {nombre_producto} no encontrado.'
    
    # Obtener los ingredientes necesarios para el producto
    ingredientes_producto = ProductoIngrediente.query.filter_by(producto_id=producto.id).all()
    
    # Verificar si hay suficiente inventario para cada ingrediente
    for pi in ingredientes_producto:
        ingrediente = Ingrediente.query.get(pi.ingrediente_id)
        if ingrediente.inventario < pi.cantidad:
            return f'¡Oh no! Nos hemos quedado sin {ingrediente.nombre}.'
    
    # Si todos los ingredientes están disponibles, actualizar el inventario
    for pi in ingredientes_producto:
        ingrediente = Ingrediente.query.get(pi.ingrediente_id)
        ingrediente.inventario -= pi.cantidad
        db.session.add(ingrediente)
    
    # Confirmar la venta (puedes agregar lógica adicional para registrar la venta, etc.)
    db.session.commit()
    
    return f'Producto {nombre_producto} vendido con éxito.'
