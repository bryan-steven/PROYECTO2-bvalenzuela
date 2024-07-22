import unittest
from flask import Flask
from models.database import db, Ingrediente, Producto, ProductoIngrediente
from models.heladeria import Heladeria
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación Flask para pruebas
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usa una base de datos en memoria para pruebas
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestHeladeria(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Configura el entorno de pruebas para la aplicación y la base de datos."""
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestingConfig)
        db.init_app(cls.app)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        with cls.app.app_context():
            db.create_all()
        cls.heladeria = Heladeria()

    @classmethod
    def tearDownClass(cls):
        """Limpia la base de datos y el contexto de la aplicación después de todas las pruebas."""
        with cls.app.app_context():
            db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Preparación para cada prueba individual."""
        with self.app.app_context():
            # No es necesario iniciar una transacción explícita aquí
            pass

    def tearDown(self):
        """Deshacer cambios y limpiar después de cada prueba."""
        with self.app.app_context():
            db.session.rollback()  # Revertir cambios no confirmados
            db.session.remove()    # Limpiar la sesión de la base de datos

    def test_ingrediente_sano(self):
        """Prueba si un ingrediente es sano."""
        ingrediente = Ingrediente(nombre='Leche', precio=1.5, calorias=100, inventario=10, es_vegetariano=True)
        db.session.add(ingrediente)
        db.session.commit()
        self.assertTrue(ingrediente.es_vegetariano)

    def test_abastecer_ingrediente(self):
        """Prueba el abastecimiento de un ingrediente."""
        ingrediente = Ingrediente(nombre='Azúcar', precio=0.5, calorias=400, inventario=5, es_vegetariano=True)
        db.session.add(ingrediente)
        db.session.commit()
        # Simular abastecimiento
        ingrediente.inventario += 10
        db.session.commit()
        self.assertEqual(ingrediente.inventario, 15)

    def test_renovar_inventario(self):
        """Prueba la renovación del inventario."""
        ingrediente = Ingrediente(nombre='Chocolate', precio=2.0, calorias=500, inventario=0, es_vegetariano=True)
        db.session.add(ingrediente)
        db.session.commit()
        # Llamar al método para renovar inventario
        self.heladeria.renovar_inventario(ingrediente.id, 20)
        ingrediente = Ingrediente.query.get(ingrediente.id)
        self.assertEqual(ingrediente.inventario, 20)

    def test_calcular_calorias(self):
        """Prueba el cálculo de calorías en copas y malteadas."""
        leche = Ingrediente(nombre='Leche', precio=1.0, calorias=50, inventario=100, es_vegetariano=True)
        chocolate = Ingrediente(nombre='Chocolate', precio=2.0, calorias=150, inventario=50, es_vegetariano=True)
        db.session.add_all([leche, chocolate])
        db.session.commit()
        producto = Producto(nombre='Malteada Chocolate', precio_publico=8.0, tipo='Malteada', volumen=500)
        db.session.add(producto)
        db.session.commit()
        producto_ingrediente_leche = ProductoIngrediente(producto_id=producto.id, ingrediente_id=leche.id, cantidad=200)
        producto_ingrediente_chocolate = ProductoIngrediente(producto_id=producto.id, ingrediente_id=chocolate.id, cantidad=100)
        db.session.add_all([producto_ingrediente_leche, producto_ingrediente_chocolate])
        db.session.commit()
        calorias = self.heladeria.calcular_calorias(producto.id)
        self.assertEqual(calorias, 20000)  # Ajusta según tu lógica de cálculo

    def test_calcular_costo_produccion(self):
        """Prueba el cálculo del costo de producción."""
        leche = Ingrediente(nombre='Leche', precio=1.0, calorias=50, inventario=100, es_vegetariano=True)
        chocolate = Ingrediente(nombre='Chocolate', precio=2.0, calorias=150, inventario=50, es_vegetariano=True)
        db.session.add_all([leche, chocolate])
        db.session.commit()
        producto = Producto(nombre='Malteada Chocolate', precio_publico=8.0, tipo='Malteada', volumen=500)
        db.session.add(producto)
        db.session.commit()
        producto_ingrediente_leche = ProductoIngrediente(producto_id=producto.id, ingrediente_id=leche.id, cantidad=200)
        producto_ingrediente_chocolate = ProductoIngrediente(producto_id=producto.id, ingrediente_id=chocolate.id, cantidad=100)
        db.session.add_all([producto_ingrediente_leche, producto_ingrediente_chocolate])
        db.session.commit()
        costo = self.heladeria.calcular_costo_produccion(producto.id)
        self.assertEqual(costo, 300)  # Ajusta según tu lógica de cálculo

    def test_calcular_rentabilidad(self):
        """Prueba el cálculo de la rentabilidad de un producto."""
        leche = Ingrediente(nombre='Leche', precio=1.0, calorias=50, inventario=100, es_vegetariano=True)
        chocolate = Ingrediente(nombre='Chocolate', precio=2.0, calorias=150, inventario=50, es_vegetariano=True)
        db.session.add_all([leche, chocolate])
        db.session.commit()
        producto = Producto(nombre='Malteada Chocolate', precio_publico=10.0, tipo='Malteada', volumen=500)
        db.session.add(producto)
        db.session.commit()
        producto_ingrediente_leche = ProductoIngrediente(producto_id=producto.id, ingrediente_id=leche.id, cantidad=200)
        producto_ingrediente_chocolate = ProductoIngrediente(producto_id=producto.id, ingrediente_id=chocolate.id, cantidad=100)
        db.session.add_all([producto_ingrediente_leche, producto_ingrediente_chocolate])
        db.session.commit()
        rentabilidad = self.heladeria.calcular_rentabilidad(producto.id)
        self.assertEqual(rentabilidad, 100)  # Ajusta según tu lógica de cálculo

    def test_producto_mas_rentable(self):
        """Prueba encontrar el producto más rentable."""
        leche = Ingrediente(nombre='Leche', precio=1.0, calorias=50, inventario=100, es_vegetariano=True)
        chocolate = Ingrediente(nombre='Chocolate', precio=2.0, calorias=150, inventario=50, es_vegetariano=True)
        db.session.add_all([leche, chocolate])
        db.session.commit()
        producto1 = Producto(nombre='Malteada Chocolate', precio_publico=10.0, tipo='Malteada', volumen=500)
        producto2 = Producto(nombre='Malteada Vainilla', precio_publico=9.0, tipo='Malteada', volumen=500)
        db.session.add_all([producto1, producto2])
        db.session.commit()
        producto_ingrediente1 = ProductoIngrediente(producto_id=producto1.id, ingrediente_id=leche.id, cantidad=200)
        producto_ingrediente2 = ProductoIngrediente(producto_id=producto1.id, ingrediente_id=chocolate.id, cantidad=100)
        producto_ingrediente3 = ProductoIngrediente(producto_id=producto2.id, ingrediente_id=leche.id, cantidad=200)
        db.session.add_all([producto_ingrediente1, producto_ingrediente2, producto_ingrediente3])
        db.session.commit()
        mejor_producto = self.heladeria.producto_mas_rentable()
        self.assertEqual(mejor_producto.id, producto1.id)

    def test_vender_producto(self):
        """Prueba la venta de un producto."""
        leche = Ingrediente(nombre='Leche', precio=1.0, calorias=50, inventario=100, es_vegetariano=True)
        chocolate = Ingrediente(nombre='Chocolate', precio=2.0, calorias=150, inventario=50, es_vegetariano=True)
        db.session.add_all([leche, chocolate])
        db.session.commit()
        producto = Producto(nombre='Malteada Chocolate', precio_publico=10.0, tipo='Malteada', volumen=500)
        db.session.add(producto)
        db.session.commit()
        producto_ingrediente_leche = ProductoIngrediente(producto_id=producto.id, ingrediente_id=leche.id, cantidad=200)
        producto_ingrediente_chocolate = ProductoIngrediente(producto_id=producto.id, ingrediente_id=chocolate.id, cantidad=100)
        db.session.add_all([producto_ingrediente_leche, producto_ingrediente_chocolate])
        db.session.commit()
        # Vender el producto
        self.heladeria.vender(producto.id)
        # Verificar inventario después de la venta
        ingrediente_leche = Ingrediente.query.get(leche.id)
        ingrediente_chocolate = Ingrediente.query.get(chocolate.id)
        self.assertEqual(ingrediente_leche.inventario, 100 - 200)
        self.assertEqual(ingrediente_chocolate.inventario, 50 - 100)

if __name__ == '__main__':
    unittest.main()
