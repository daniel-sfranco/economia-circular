import unittest
from desapeg.app import app
from desapeg.extensions import db

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

    # envio inválido (sem imagem)
    def test_form_sem_imagem(self):
        response = self.client.post('/forms', data={
            'prod_name': 'Produto Teste',
            'description': 'Descrição teste',
            'price': '100.50',
            'quantity': '10'
        })

        # Não deve redirecionar (formulário inválido)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()