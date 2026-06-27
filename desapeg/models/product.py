from desapeg.extensions import db
from datetime import datetime, timezone

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    seller = db.Column(db.String(120), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True) 
    image_paths = db.Column(db.Text, nullable=True) 
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'seller': self.seller,
            'cost': self.cost,
            'post_date': self.post_date.isoformat() if self.post_date else None,
            'quantity': self.quantity,
            'description': self.description,
            'images': self.image_paths.split(',') if self.image_paths else [],
            'category': self.category.name if self.category else None
        }