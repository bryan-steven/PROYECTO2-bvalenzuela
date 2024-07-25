import unittest
from controllers.heladeria_controller import db, Producto, Ingrediente, ProductoIngrediente, get_productos

class TestGetProductos(unittest.TestCase):
    
    def test_get_productos(self):
        productos = get_productos()
        self.assertEqual(productos[0].nombre, 'Helado de Fresa')