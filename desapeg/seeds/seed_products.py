from faker import Faker
from desapeg.extensions import db
from desapeg.models.product import Product

fake = Faker('pt_BR')

def seed_products(n):
    for _ in range(n):
        product = Product(
            name = fake.word(),
            seller = fake.name(),
            cost = fake.random_number(digits=5, fix_len=True) / 100,
            post_date = fake.date_time_this_year(),
            quantity = fake.random_int(min=1, max=10),
            description = fake.sentence(),
        )
        db.session.add(product)
    db.session.commit()
    print(f'Seeded {n} products.')