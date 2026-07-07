import unittest
import io
from PIL import Image
from desapeg.app import app
from desapeg.extensions import db
from desapeg.models.category import Category
from desapeg.models.product import Product

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
            for name in ['Móveis', 'Eletrodomésticos']:
                if not Category.query.filter_by(name=name).first():
                    db.session.add(Category(name=name))
            db.session.commit()

            response = self.client.post(
            '/forms',
            data={
                'prod_name': 'Produto Teste',
                'description': 'Descrição muito legal',
                'quantity': '10',
                'price': '50.50',
                'condition': 'Novo',
                'usage_time': 'Nunca usado',
                'pickup_location': 'Campinas',
                'images': (create_test_image(), 'test.jpg'),
                'categories': 'Móveis'
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_product(self):
        response = self.client.post(
            '/forms',
            data={
                'prod_name': 'Produto 2',
                'description': 'Descrição muito legal',
                'quantity': '10',
                'price': '100.50',
                'condition': 'Novo',
                'usage_time': 'Nunca usado',
                'pickup_location': 'Campinas',
                'images': (create_test_image(), 'test.jpg'),
                'categories': 'Móveis, Eletrodomésticos'
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )

        # 1. Verifica redirect
        self.assertEqual(response.status_code, 302)

        # 2. Verifica o produto no banco de dados
        with app.app_context():
            product = Product.query.order_by(Product.id.desc()).first()

            categories = [category.name for category in product.categories]
            categories.sort()

            self.assertIsNotNone(product)
            self.assertEqual(product.name, 'Produto 2')
            self.assertEqual(product.description, 'Descrição muito legal')
            self.assertEqual(product.quantity, 10)
            self.assertEqual(product.cost, 100.50)
            self.assertEqual(product.condition, 'Novo')
            self.assertEqual(product.usage_time, 'Nunca usado')
            self.assertEqual(product.pickup_location, 'Campinas')
            self.assertEqual(categories, ['Eletrodomésticos', 'Móveis'])

    def test_update_product(self):
        response = self.client.put(
            '/api/product/1',
            data={
                'name': 'Produto 2',
                'description': 'Descrição muito legal',
                'condition': 'Novo',
                'cost': '100.50',
                'quantity': '10',
                'usage_time': 'Nunca usado',
                'pickup_location': 'Indaiatuba',
                'images': (create_test_image(), 'test.jpg'),
                'categories': 'Móveis'
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )

        # 1. Verifica redirect
        self.assertEqual(response.status_code, 200)

        # 2. Verifica o produto no banco de dados
        with app.app_context():
            product = Product.query.first()

            self.assertIsNotNone(product)
            self.assertEqual(product.name, 'Produto 2')
            self.assertEqual(product.description, 'Descrição muito legal')
            self.assertEqual(product.quantity, 10)
            self.assertEqual(product.cost, 100.50)
            self.assertEqual(product.condition, 'Novo')
            self.assertEqual(product.usage_time, 'Nunca usado')
            self.assertEqual(product.pickup_location, 'Indaiatuba')
            self.assertEqual([category.name for category in product.categories], ['Móveis'])

    def test_delete_product(self):
        response = self.client.delete(
            "api/product/1"
        )

        self.assertEqual(response.status_code, 200)

        with app.app_context():
            products = Product.query.count()
            self.assertEqual(products, 0)


if __name__ == '__main__':
    unittest.main()