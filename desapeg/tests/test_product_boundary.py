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

class ProductBoundaryTestCase(unittest.TestCase):

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

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def get_base_payload(self):
        # Retorna um dicionário com dados válidos para facilitar os testes.
        return {
            'name': 'Produto Teste',
            'description': 'Descrição super incrível do produto',
            'quantity': '10',
            'cost': '50.50',
            'condition': 'Novo',
            'usage_time': 'Nunca usado',
            'pickup_location': 'Barão Geraldo, Campinas',
            'images': (create_test_image(), 'test.jpg'),
            'categories': 'Móveis'
        }

    def test_boundary_prod_name_length(self):
        # Testa o limite de tamanho do texto do nome do produto (máximo 50 caracteres)
        boundaries = {
            '': 200, # 0 caracteres
            'A': 302, # 1 caractere
            'A' * 50: 302, # exatamente 50 caracteres
            'A' * 51: 200 # 51 caracteres
        }

        for name, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['name'] = name
            
            response = self.client.post(
                '/forms',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            self.assertEqual(response.status_code, expected_status, f"Falha no comprimento do nome com {len(name)} caracteres")

    def test_boundary_description_length(self):
        # Testa o limite de tamanho do texto da descrição (0 e máximo 5000 caracteres)
        boundaries = {
            '': 200, # 0 caracteres
            'A': 302, # 1 caractere
            'A' * 5000: 302, # exatamente 5000 caracteres
            'A' * 5001: 200 # 5001 caracteres
        }

        for desc, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['description'] = desc
            
            response = self.client.post(
                '/forms',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            self.assertEqual(response.status_code, expected_status, f"Falha no comprimento da descrição com {len(desc)} caracteres")

    def test_boundary_price_decimal_places(self):
        # Testa o limite de casas decimais (máximo 2)
        payload = self.get_base_payload()
        payload['cost'] = '10.123' # 3 casas decimais
        
        response = self.client.post(
            '/forms',
            data=payload,
            content_type='multipart/form-data',
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 200, "Falha na validação de casas decimais do preço.")

    def test_boundary_quantity(self):
        # Testa os valores limites para a quantidade (0 a 50)
        boundaries = {
            '-1': 200, # abaixo do mínimo
            '0': 200, # abaixo do mínimo
            '1': 302, # limite mínimo
            '50': 302, # limite máximo
            '51': 200 # acima do máximo
        }

        for quantity, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['quantity'] = quantity
            
            response = self.client.post(
                '/forms',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            self.assertEqual(response.status_code, expected_status, f"Falha na quantidade limite: {quantity}")

    def test_boundary_price(self):
        # Testa os valores limites para o preço (0.0 a 10000.0)
        boundaries = {
            '-0.01': 200, # abaixo do mínimo
            '0.00': 302, # limite mínimo
            '10000.00': 302, # limite máximo
            '10000.01': 200, # acima do máximo
        }

        for cost, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['cost'] = cost
            
            response = self.client.post(
                '/forms',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            self.assertEqual(response.status_code, expected_status, f"Falha no preço limite: {cost}")

    def test_boundary_images(self):
        # Testa os limites de envio de imagens
        boundaries = {
            0: 200, # obrigatório pelo menos 1 imagem
            1: 302, # mínimo de 1 imagem
            5: 302, # limite máximo de 5 imagens
            6: 200 # ultrapassa o limite de 5 imagens
        }

        for num_images, expected_status in boundaries.items():
            payload = self.get_base_payload()
            
            if num_images == 0:
                # Simula o envio de um campo de arquivo vazio
                payload['images'] = (io.BytesIO(b''), '')
            else:
                images_list = []
                for i in range(num_images):
                    images_list.append((create_test_image(), f'test{i}.jpg'))
                payload['images'] = images_list
            
            response = self.client.post(
                '/forms',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            self.assertEqual(
                response.status_code, 
                expected_status, 
                f"Falha na validação com {num_images} imagens."
            )

if __name__ == '__main__':
    unittest.main()