from desapeg.extensions import db
from product_review import ProductReview

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rating_avg = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)
    
    # O 'backref' cria a propriedade 'owner' no objeto Product.
    products = db.relationship('Product', foreign_keys="Product.user_id", backref='owner', lazy=True)

    # REFATORAÇÃO (Feature Envy): 
    # A responsabilidade de calcular a média de avaliações foi movida do controller (routes.py) 
    # para o próprio modelo (User).
    def update_rating(self):
        reviews = ProductReview.query.filter_by(target_user_id=self.id).all()
        self.rating_count = len(reviews)
        
        if self.rating_count > 0:
            self.rating_avg = round(sum(review.score for review in reviews) / self.rating_count, 1)
        else:
            self.rating_avg = 0.0

    def __repr__(self):
        return f'<User {self.name}>'