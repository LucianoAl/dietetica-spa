# tests/test_api.py
import unittest
import os
import sys

# Se ajusta el path para importar desde la raíz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_dietetica import app, init_db, DB_NAME

class TestDieteticaAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Se inicializa la base de datos antes de las pruebas
        init_db()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_1_listar_productos(self):
        respuesta = self.app.get('/productos')
        self.assertEqual(respuesta.status_code, 200)
        # Se verifica la carga de productos
        self.assertIn(b'Caja barra Laddubar', respuesta.data)

    def test_2_agregar_al_carrito(self):
        # Se prueba la inserción de un ítem
        respuesta = self.app.post('/carrito/1')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'Agregado', respuesta.data)

    def test_3_calcular_total(self):
        # Se verifica el cálculo del total
        self.app.post('/carrito/2') 
        respuesta = self.app.get('/carrito/total')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'carrito', respuesta.data)

    def test_4_eliminar_del_carrito(self):
        # Se prueba la eliminación de un ítem
        self.app.post('/carrito/3')
        res_total = self.app.get('/carrito/total').get_json()
        item_id = res_total['carrito'][0]['id_carrito']
        
        respuesta = self.app.delete(f'/carrito/{item_id}')
        self.assertEqual(respuesta.status_code, 200)

if __name__ == '__main__':
    unittest.main()