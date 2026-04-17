import os
from flask import Flask
from .extensions import db
from .routes import *
from .models.product import Product

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "mock.db")}'
app.config['SECRET_KEY'] = 'chave_random_pra_testar'
db.init_app(app)

app.register_blueprint(main_routes)


if __name__ == "__main__":
    app.run(debug = True)