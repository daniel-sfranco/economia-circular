import unittest
import io
from PIL import Image
from desapeg.app import app
from desapeg.extensions import db
from desapeg.tests.test_utils import create_test_image

class ProductFormTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_form_submission_valid(self):
        # Simula upload de imagem para criar um produto
        data = {
                'name': 'Produto Teste',
                'description': 'Descrição muito legal',
                'quantity': '10',
                'cost': '100.50',
                'condition': 'Novo',
                'usage_time': 'Nunca usado',
                'pickup_location': 'Campinas',
                'images': (create_test_image(), 'test.jpg'),
                'categories': 'Móveis, Eletrodomésticos'
        }

        response = self.client.post(
            '/forms',
            data=data,
            content_type='multipart/form-data',
            follow_redirects=False
        )

        # Deve redirecionar (formulário válido)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/forms', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()