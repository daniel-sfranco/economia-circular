from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mock.db'
db = SQLAlchemy(app)

app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug = True)