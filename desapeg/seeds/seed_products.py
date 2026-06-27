import random
from faker import Faker
from desapeg.extensions import db
from desapeg.models.product import Product
from desapeg.models.category import Category

fake = Faker('pt_BR')

def seed_products(n):
    categorias = Category.query.all()
    
    if not categorias:
        print("Erro: Nenhuma categoria no banco")
        return

    for _ in range(n):
        product = Product(
            name = fake.word(),
            seller = fake.name(),
            cost = fake.random_number(digits=5, fix_len=True) / 100,
            post_date = fake.date_time_this_year(),
            quantity = fake.random_int(min=1, max=10),
            description = fake.sentence(),
            category = random.choice(categorias)
        )
        db.session.add(product)
    
    db.session.commit()
    print(f'Seeded {n} products.')