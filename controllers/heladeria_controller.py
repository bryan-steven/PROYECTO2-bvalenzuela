from models.database import db, Producto, Ingrediente, ProductoIngrediente

def get_productos():
    productos = Producto.query.all()
    #print(productos[0].ingredientes)
    return productos

def get_ingredientes():
    ingredientes = Ingrediente.query.all()
    return ingredientes

def es_sano():
    ingredientes = Ingrediente.query.all()
    resultados = {}
    for ingrediente in ingredientes:
        sano = ingrediente.es_sano()
        resultados[ingrediente.nombre] = sano
    return resultados

def calcular_calorias():
    productos = Producto.query.all()
    resultados = {}
    for producto in productos:
        calorias = producto.calcular_calorias()
        resultados[producto.nombre] = calorias
    return resultados

def producto_mas_rentable():
    productos = Producto.query.all()
    if not productos:
        return None
    mejor_producto = productos[0]
    for producto in productos:
        if producto.calcular_rentabilidad() > mejor_producto.calcular_rentabilidad():
            mejor_producto = producto
    return mejor_producto