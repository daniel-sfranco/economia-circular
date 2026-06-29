from desapeg.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # O 'backref' cria a propriedade 'owner' no objeto Product.
    products = db.relationship('Product', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'