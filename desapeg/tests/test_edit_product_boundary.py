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

class ProductEditBoundaryTestCase(unittest.TestCase):

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
            
            # 1. Criação de um produto inicial que será editado
            produto = Product(
                name="Produto Original",
                description="Descrição original",
                quantity=5,
                cost=10.00,
                condition="Novo",
                usage_time="Nenhum",
                pickup_location="Local X",
                user_id=1
            )
            db.session.add(produto)
            db.session.commit()
            
            # ID para a rota do PUT
            self.product_id = produto.id 

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def get_base_payload(self):

        return {
            'name': 'Produto Teste Editado',
            'description': 'Descrição super incrível do produto modificada',
            'quantity': '10',
            'cost': '50.50',
            'condition': 'Usado',
            'usage_time': 'Nunca usado',
            'pickup_location': 'Barão Geraldo, Campinas',
            'images': (create_test_image(), 'test.jpg'),
            'categories': 'Móveis',
        }

    def test_boundary_prod_name_length_on_edit(self):
        # Testa o limite de tamanho do texto do nome do produto (máximo 50 caracteres)
        boundaries = {
            '': 400, # Inválido
            'A': 200, # Válido
            'A' * 50: 200, # Válido
            'A' * 51: 400 # Inválido
        }

        for name, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['name'] = name
            
            response = self.client.put(
                f'/api/product/{self.product_id}',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            
            self.assertEqual(
                response.status_code, 
                expected_status, 
                f"Falha na edição: comprimento do nome com {len(name)} caracteres retornou {response.status_code}"
            )

    def test_boundary_description_length_on_edit(self):
            # Testa o limite de tamanho do texto da descrição (0 e máximo 5000 caracteres)
            boundaries = {
                '': 400,
                'A': 200,
                'A' * 5000: 200,
                'A' * 5001: 400
            }

            for desc, expected_status in boundaries.items():
                payload = self.get_base_payload()
                payload['description'] = desc

                response = self.client.put(
                    f'/api/product/{self.product_id}',
                    data=payload,
                    content_type='multipart/form-data',
                    follow_redirects=False
                )
                self.assertEqual(
                    response.status_code, 
                    expected_status, 
                    f"Falha na edição: comprimento da descrição com {len(desc)} caracteres retornou {response.status_code}"
                )

    def test_boundary_price_decimal_places_on_edit(self):
        # Testa o limite de casas decimais do preço (máximo 2)
        payload = self.get_base_payload()
        payload['cost'] = '10.123'
        
        response = self.client.put(
            f'/api/product/{self.product_id}',
            data=payload,
            content_type='multipart/form-data',
            follow_redirects=False
        )
        
        self.assertEqual(
            response.status_code, 
            400, 
            f"Falha na edição: validação de casas decimais do preço retornou {response.status_code} ao invés de erro."
        )

    def test_boundary_quantity_on_edit(self):
        # Testa os valores limites para a quantidade (0 a 50)
        boundaries = {
            '-1': 400,
            '0': 400,
            '50': 200,
            '51': 400
        }

        for quantity, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['quantity'] = quantity
            
            response = self.client.put(
                f'/api/product/{self.product_id}',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            self.assertEqual(
                response.status_code, 
                expected_status, 
                f"Falha na edição: quantidade limite de {quantity} retornou {response.status_code}"
            )

    def test_boundary_price_on_edit(self):
        # Testa os valores limites para o preço (0.0 a 10000.0)
        boundaries = {
            '-0.01': 400,
            '0.00': 200,
            '10000.00': 200,
            '10000.01': 400,
        }

        for price, expected_status in boundaries.items():
            payload = self.get_base_payload()
            payload['cost'] = price
            
            response = self.client.put(
                f'/api/product/{self.product_id}',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            self.assertEqual(
                response.status_code, 
                expected_status, 
                f"Falha na edição: preço limite de {price} retornou {response.status_code}"
            )

    def test_boundary_images_on_edit(self):
        # Testa os limites de envio de imagens (1 a 5)
        boundaries = {
            0: 200,
            1: 200,
            5: 200,
            6: 400
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
            
            response = self.client.put(
                f'/api/product/{self.product_id}',
                data=payload,
                content_type='multipart/form-data',
                follow_redirects=False
            )
            self.assertEqual(
                response.status_code, 
                expected_status, 
                f"Falha na edição: validação com {num_images} imagens retornou {response.status_code}"
            )