import unittest
import io
from PIL import Image
from app import app
from extensions import db
from models.product import Product

# Função auxiliar para criar uma imagem válida em memória
def create_test_image():
    img = Image.new('RGB', (10, 10), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

class ProductDBTestCase(unittest.TestCase):

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

    def test_product_saved_in_db(self):
        response = self.client.post(
            '/forms',
            data={
                'prod_name': 'Produto Teste',
                'description': 'Descrição muito legal',
                'price': '100.50',
                'quantity': '10',
                'images': (create_test_image(), 'test.jpg')
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )

        # 1. Verifica redirect
        self.assertEqual(response.status_code, 302)

        # 2. Verifica o produto no banco de dados
        with app.app_context():
            product = Product.query.first()

            self.assertIsNotNone(product)
            self.assertEqual(product.name, 'Produto Teste')
            self.assertEqual(product.cost, 100.50)
            self.assertEqual(product.quantity, 10)
            self.assertEqual(product.description, 'Descrição muito legal')

if __name__ == '__main__':
    unittest.main()