import tempfile
import unittest
from pathlib import Path
from data import database

class DatabaseTest(unittest.TestCase):
    def test_validation_and_delete(self):
        original = database.DB_NAME
        try:
            with tempfile.TemporaryDirectory() as temp:
                database.DB_NAME = Path(temp) / 'test.db'
                database.init_db()
                self.assertFalse(database.adicionar_transacao('Entrada', 'Salario', float('inf'), '2026-01-01'))
                self.assertFalse(database.adicionar_transacao('Entrada', 'Salario', 1, '2026-02-31'))
                self.assertTrue(database.adicionar_transacao('Entrada', 'Salario', 10, '2026-01-01'))
                rows = database.listar_transacoes(1, 2026)
                self.assertEqual(len(rows), 1)
                self.assertTrue(database.deletar_transacao(rows[0][0]))
                self.assertFalse(database.deletar_transacao(rows[0][0]))
        finally:
            database.DB_NAME = original
