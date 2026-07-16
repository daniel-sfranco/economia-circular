import io
import json
import unittest
from PIL import Image
from desapeg.app import app
from desapeg.extensions import db
from desapeg.builders.product_search_builder import ProductSearchBuilder
from desapeg.models.category import Category

def create_test_image():
    img = Image.new('RGB', (10, 10), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

class SearchFilterTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

            for name in ["Móveis", "Eletrodomésticos"]:
                if not db.session.query(Category).filter_by(name=name).first():
                    db.session.add(Category(name=name))

            db.session.commit()
        
        response = self.client.post(
            '/forms',
            data={
                'name': 'Produto Teste',
                'description': 'Descrição muito legal',
                'quantity': '10',
                'cost': '50.50',
                'condition': 'Novo',
                'usage_time': 'Nunca usado',
                'pickup_location': 'Campinas',
                'images': (create_test_image(), 'test.jpg'),
                'categories': 'Eletrodomésticos'
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )
        response = self.client.post(
            '/forms',
            data={
                'name': 'Produto 2',
                'description': 'Descrição muito legal',
                'quantity': '10',
                'cost': '100.50',
                'condition': 'Novo',
                'usage_time': 'Nunca usado',
                'pickup_location': 'Campinas',
                'images': (create_test_image(), 'test.jpg'),
                'categories': 'Móveis, Eletrodomésticos'
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_search_route(self):
        response = self.client.get("/search?q=Produto%20Teste")
        self.assertEqual(response.status_code, 200)
    
    def test_filter_string(self):
        with app.app_context():
            produtos = (
                ProductSearchBuilder()
                .with_text("Produto Teste")
                .build()
                .all()
            )
            self.assertEqual(produtos[0].name, "Produto Teste")

    def test_filter_range(self):
        with app.app_context():
            produtos = (
                ProductSearchBuilder()
                .with_price_range(100, 500)
                .build()
                .all()
            )
            self.assertEqual(produtos[0].name, "Produto 2")
            produtos = (
                ProductSearchBuilder()
                .with_price_range(10, 100)
                .build()
                .all()
            )
            self.assertEqual(produtos[0].name, "Produto Teste")

    def test_filter_list(self):
        with app.app_context():
            produtos = (
                ProductSearchBuilder()
                .with_categories(["Móveis"])
                .build()
                .all()
            )
            self.assertEqual(produtos[0].name, "Produto 2")


if __name__ == "__main__":
    unittest.main()