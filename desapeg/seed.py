from desapeg.app import app
from desapeg.extensions import db
from desapeg.models.product import Product
from desapeg.seeds.seed_products import seed_products

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_products(20)
        print("Database seeded with products.")

if __name__ == "__main__":
    seed()