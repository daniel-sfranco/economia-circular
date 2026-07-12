import io
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

        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        categories_list = [
            "Móveis", "Eletrodomésticos", "Utensílios", "Cama, Mesa e Banho", 
            "Eletrônicos e Informática", "Livros e Materiais Acadêmicos", 
            "Papelaria", "Roupas", "Transporte/Mobilidade", "Jogos", 
            "Limpeza", "Outros"
        ]

        for name in categories_list:
            if not db.session.query(Category).filter_by(name=name).first():
                db.session.add(Category(name=name))

        db.session.commit()
        
        self.client.post(
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
                'categories': 'Eletrodomésticos'
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )
        self.client.post(
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
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

    # Testes pairwise com particionamento para filtros
    def test_pairwise_combinations(self):
        pairwise_cases = [
            ("Móveis", "Baixo", "Vazio"),
            ("Móveis", "Médio", "Preenchido"),
            ("Móveis", "Alto", "Preenchido"),
            ("Eletrodomésticos", "Baixo", "Preenchido"),
            ("Eletrodomésticos", "Médio", "Vazio"),
            ("Eletrodomésticos", "Alto", "Vazio"),
            ("Utensílios", "Baixo", "Preenchido"),
            ("Utensílios", "Médio", "Vazio"),
            ("Utensílios", "Alto", "Preenchido"),
            ("Cama, Mesa e Banho", "Baixo", "Preenchido"),
            ("Cama, Mesa e Banho", "Médio", "Vazio"),
            ("Cama, Mesa e Banho", "Alto", "Preenchido"),
            ("Eletrônicos e Informática", "Baixo", "Vazio"),
            ("Eletrônicos e Informática", "Médio", "Preenchido"),
            ("Eletrônicos e Informática", "Alto", "Vazio"),
            ("Livros e Materiais Acadêmicos", "Baixo", "Preenchido"),
            ("Livros e Materiais Acadêmicos", "Médio", "Vazio"),
            ("Livros e Materiais Acadêmicos", "Alto", "Vazio"),
            ("Papelaria", "Baixo", "Preenchido"),
            ("Papelaria", "Médio", "Vazio"),
            ("Papelaria", "Alto", "Vazio"),
            ("Roupas", "Baixo", "Vazio"),
            ("Roupas", "Médio", "Preenchido"),
            ("Roupas", "Alto", "Preenchido"),
            ("Transporte/Mobilidade", "Baixo", "Vazio"),
            ("Transporte/Mobilidade", "Médio", "Preenchido"),
            ("Transporte/Mobilidade", "Alto", "Preenchido"),
            ("Jogos", "Baixo", "Preenchido"),
            ("Jogos", "Médio", "Vazio"),
            ("Jogos", "Alto", "Vazio"),
            ("Limpeza", "Baixo", "Preenchido"),
            ("Limpeza", "Médio", "Vazio"),
            ("Limpeza", "Alto", "Preenchido"),
            ("Outros", "Baixo", "Preenchido"),
            ("Outros", "Médio", "Vazio"),
            ("Outros", "Alto", "Vazio")
        ]

        price_map = {
            "Baixo": (0, 50),
            "Médio": (51, 200),
            "Alto": (201, 5000)
        }

        text_map = {
            "Vazio": "",
            "Preenchido": "Produto"
        }

        with app.app_context():
            for category, price_range, text in pairwise_cases:
                min_price, max_price = price_map[price_range]
                search_text = text_map[text]

                with self.subTest(category=category, preco=price_range, text=text):
                    print(f"Pairwise -> Categoria: {category} | Preço: {price_range} | Texto: '{text}'")
                    produtos_encontrados = (
                        ProductSearchBuilder()
                        .with_text(search_text)
                        .with_categories([category])
                        .with_price_range(min_price, max_price)
                        .build()
                        .all()
                    )
                    
                    self.assertIsInstance(produtos_encontrados, list)

if __name__ == "__main__":
    unittest.main()