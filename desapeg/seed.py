from app import app
from extensions import db
from models.product import Product
from seeds.seed_products import seed_products

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_products(20)