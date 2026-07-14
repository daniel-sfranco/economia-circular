from desapeg.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rating_avg = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)
    
    # O 'backref' cria a propriedade 'owner' no objeto Product.
    products = db.relationship('Product', foreign_keys="Product.user_id", backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'