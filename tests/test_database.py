import unittest
import copy
import csv
from gestor import database as db
from gestor import helpers
from gestor import config

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

    def test_escritura_csv(self):
        # Borrar y modificar para comprobar cambios
        db.Clientes.borrar('48H')
        db.Clientes.modificar('28Z', 'Mariana', 'Pérez')

        # Leer del CSV y verificar que los cambios están guardados
        with open(config.DATABASE_PATH, newline="\n") as fichero:
            reader = csv.reader(fichero, delimiter=";")
            filas = list(reader)

        # Debe haber 2 clientes ahora
        self.assertEqual(len(filas), 2)

        # Buscar si Mariana está en el CSV
        encontrados = [fila for fila in filas if fila[1] == 'Mariana' and fila[2] == 'Pérez']
        self.assertTrue(encontrados)

if __name__ == "__main__":
    unittest.main()
