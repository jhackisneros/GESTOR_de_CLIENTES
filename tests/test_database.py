import unittest
import copy
from gestor import database as db
from gestor import helpers

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('15J', 'Marta', 'Perez'),
            db.Cliente('48H', 'Manolo', 'Lopez'),
            db.Cliente('28Z', 'Ana', 'Garcia')
        ]

    def test_buscar_cliente(self):
        self.assertIsNotNone(db.Clientes.buscar('15J'))
        self.assertIsNone(db.Clientes.buscar('99X'))

    def test_crear_cliente(self):
        nuevo = db.Clientes.crear('99Z', 'Lucas', 'Santos')
        self.assertEqual(nuevo.dni, '99Z')
        self.assertEqual(len(db.Clientes.lista), 4)

    def test_modificar_cliente(self):
        db.Clientes.modificar('28Z', 'Mariana', 'Pérez')
        mod = db.Clientes.buscar('28Z')
        self.assertEqual(mod.nombre, 'Mariana')

    def test_borrar_cliente(self):
        db.Clientes.borrar('48H')
        self.assertIsNone(db.Clientes.buscar('48H'))

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('48H', db.Clientes.lista))  # ya existe

if __name__ == "__main__":
    unittest.main()
