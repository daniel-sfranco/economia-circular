from desapeg.app import app
from desapeg.extensions import db
from desapeg.models.product import Product
from desapeg.models.user import User
from desapeg.seeds.seed_products import seed_products
from desapeg.seeds.seed_categories import seed_categories
from desapeg.seeds.seed_users import seed_users

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        seed_categories()
        seed_users(10)
        seed_products(20)
        
        print("Database seeded with products.")

if __name__ == "__main__":
    seed()