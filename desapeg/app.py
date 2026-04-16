from flask import Flask
from extensions import db
from routes import *
from models.product import Product

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:desapegunicamp123@localhost:5432/desapegunicamp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(main_routes)


if __name__ == "__main__":
    app.run(debug = True)