import unittest
from desapeg.app import app
from desapeg.extensions import db
from desapeg.models.user import User
from desapeg.models.product import Product

class EvaluationBoundaryTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            if not User.query.filter_by(id=1).first():
                seller = User(id=1, name='Vendedor Teste', email='vendedor@teste.com', phone='19999999999')
                db.session.add(seller)
            
            if not Product.query.filter_by(id=1).first():
                product = Product(
                    id=1, 
                    name='Produto Teste', 
                    user_id=1, 
                    cost=10.0, 
                    quantity=1,
                    condition='Novo',
                    description='Descrição do produto teste',
                    usage_time='Nunca usado',
                    pickup_location='Barão Geraldo'
                )
                db.session.add(product)
            
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def get_base_payload(self):
        return {
            'rating': '5',
            'comment': 'Negociação perfeita!',
            'seller_id': '1',
            'product_id': '1'
        }

    def test_boundary_rating_value(self):
        # Testa a análise de limite da nota: comentários com 0, 1, 5 e 6 estrelas
        boundaries = {
            '0': 200,
            '1': 302,
            '5': 302,
            '6': 200
        }

        for rating, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['rating'] = rating
            
            response = self.client.post(
                '/evaluate',
                data=payload,
                follow_redirects=False
            )
            self.assertEqual(
                response.status_code, 
                expected_status, 
                f"Falha na validação do limite de estrelas com valor: {rating}"
            )

    def test_boundary_comment_length(self):
        # Testa a análise de limite do texto: comentários com 0, 1, 80 e 81 caracteres
        boundaries = {
            '': 302,
            'A': 302,
            'A' * 80: 302,
            'A' * 81: 200
        }

        for comment, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['comment'] = comment
            
            response = self.client.post(
                '/evaluate',
                data=payload,
                follow_redirects=False
            )
            self.assertEqual(
                response.status_code, 
                expected_status, 
                f"Falha na validação do comprimento do comentário com {len(comment)} caracteres"
            )

if __name__ == '__main__':
    unittest.main()