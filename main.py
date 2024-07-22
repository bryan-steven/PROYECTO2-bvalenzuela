from models.base import Base
from models.complemento import Complemento
from models.copa import Copa
from models.malteada import Malteada
from models.heladeria import Heladeria
from models.funciones import es_sano, calcular_calorias, calcular_costo, calcular_rentabilidad, mejor_producto

# Crear ingredientes
helado_fresa = Base(1200, 90, "Helado de Fresa", 10, True, "Fresa")
chispas_chocolate = Complemento(500, 200, "Chispas de chocolate", 20, True)
mani_japones = Complemento(900, 250, "Mani Japonés", 15, False)

# Verificar si los ingredientes son sanos
print(f"{helado_fresa._nombre} es sano: {es_sano(helado_fresa._calorias, helado_fresa._es_vegetariano)}")
print(f"{chispas_chocolate._nombre} es sano: {es_sano(chispas_chocolate._calorias, chispas_chocolate._es_vegetariano)}")

# Crear productos
copa_fresa = Copa("Copa de Fresa", 7500, "Plástico", [helado_fresa, chispas_chocolate, mani_japones])
malteada_choco = Malteada("Malteada Choco", 8000, 16, [helado_fresa, chispas_chocolate, mani_japones])

# Verificar cálculos de costos y rentabilidad
print(f"Costo de Copa de Fresa: {copa_fresa.calcular_costo()}")
print(f"Rentabilidad de Copa de Fresa: {copa_fresa.calcular_rentabilidad()}")
print(f"Calorías de Copa de Fresa: {copa_fresa.calcular_calorias()}")

print(f"Costo de Malteada Choco: {malteada_choco.calcular_costo()}")
print(f"Rentabilidad de Malteada Choco: {malteada_choco.calcular_rentabilidad()}")
print(f"Calorías de Malteada Choco: {malteada_choco.calcular_calorias()}")

# Crear heladería con la lista de productos
heladeria = Heladeria([copa_fresa, malteada_choco])

# Listar productos
for producto in heladeria._productos:
    print(f"Producto: {producto._nombre}, Precio: {producto._precio_publico}")

# Obtener el producto más rentable
producto_rentable = heladeria.producto_mas_rentable()
print("Producto más rentable:", producto_rentable)

# Probar la función vender
nombre_producto = "Copa de Fresa"
venta_exitosa = heladeria.vender(nombre_producto)
print(f"Venta de {nombre_producto}: {'Exitosa' if venta_exitosa else 'Fallida'}")

# Verificar el inventario después de la venta
print(f"Inventario de {helado_fresa._nombre} después de la venta: {helado_fresa._inventario}")
print(f"Inventario de {chispas_chocolate._nombre} después de la venta: {chispas_chocolate._inventario}")
print(f"Inventario de {mani_japones._nombre} después de la venta: {mani_japones._inventario}")

# Pruebas adicionales
ingrediente1 = {"nombre": "Helado de Fresa", "precio": 1200}
ingrediente2 = {"nombre": "Chispas de chocolate", "precio": 500}
ingrediente3 = {"nombre": "Mani Japonés", "precio": 900}

calorias = es_sano(90, False)
print(f"¿Es sano?: {calorias}")

calorias_producto = calcular_calorias([120, 150, 200])
print(f"Calorías del producto: {calorias_producto}")

costo = calcular_costo(ingrediente1, ingrediente2, ingrediente3)
print(f"Costo del producto: {costo}")

rentabilidad = calcular_rentabilidad(7500, ingrediente1, ingrediente2, ingrediente3)
print(f"Rentabilidad del producto: {rentabilidad}")

producto1 = {"nombre": "Samurai de fresas", "rentabilidad": 4900}
producto2 = {"nombre": "Samurai de mandarinas", "rentabilidad": 2500}
producto3 = {"nombre": "Malteda chocoespacial", "rentabilidad": 11000}
producto4 = {"nombre": "Cupihelado", "rentabilidad": 3200}

mejor = mejor_producto(producto1, producto2, producto3, producto4)
print(f"El mejor producto es: {mejor}")