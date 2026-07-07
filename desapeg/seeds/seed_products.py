import random
from faker import Faker
from desapeg.extensions import db
from desapeg.models.product import Product
from desapeg.models.category import Category
from desapeg.models.user import User

fake = Faker('pt_BR')

def seed_products(n):
    categories = Category.query.all()
    users = User.query.all()
    
    if not categories or not users:
        print("Erro: Crie as categorias e os usuários antes dos produtos.")
        return

    condicoes = ["Novo", "Seminovo", "Usado - Bom estado", "Usado - Marcas de uso"]
    tempos_uso = ["Menos de 1 mês", "3 meses", "6 meses", "1 ano", "Mais de 2 anos"]

    for _ in range(n):
        n_categories = random.randint(1, min(3, len(categories)))
        selected_categories = random.sample(categories, n_categories)
        
        dono_aleatorio = random.choice(users)

        product = Product(
            name = fake.word().capitalize(),
            user_id = dono_aleatorio.id,
            cost = fake.random_number(digits=5, fix_len=True) / 100,
            post_date = fake.date_time_this_year(),
            quantity = fake.random_int(min=1, max=10),
            description = fake.text(max_nb_chars=150),
            condition = random.choice(condicoes),
            pickup_location = " ".join(fake.address().split()),
            usage_time = random.choice(tempos_uso),
            categories = selected_categories
        )
        db.session.add(product)
    
    db.session.commit()
    print(f'{n} produtos inseridos com sucesso.')