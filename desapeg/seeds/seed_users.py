from faker import Faker
from desapeg.extensions import db
from desapeg.models.user import User

fake = Faker('pt_BR')

def seed_users(n=10):
    for _ in range(n):
        user = User(
            name=fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number()
        )
        db.session.add(user)
        
    db.session.commit()
    print(f"{n} usuários inseridos com sucesso.")