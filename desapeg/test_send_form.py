import unittest
import io
from app import app
from extensions import db

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
            'prod_name': 'Produto Teste',
            'description': 'Descrição teste',
            'price': '100.00',
            'quantity': '10',
            'images': (io.BytesIO(b"uma imagem bonita"), 'test.jpg')
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