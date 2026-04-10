import unittest
import os

class TestDB(unittest.TestCase):
    def test_exists_product_file(self):
        path_json = os.path.join(os.path.dirname(__file__), '..', 'fakeDB/produtos.json')
        self.assertTrue(os.path.exists(path_json), "O arquivo produtos.json não existe")
