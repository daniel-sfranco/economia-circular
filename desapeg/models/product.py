from desapeg.extensions import db
from datetime import datetime, timezone

product_category = db.Table('product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True) 
    image_paths = db.Column(db.Text, nullable=True) 
    condition = db.Column(db.String(100), nullable=False)
    pickup_location = db.Column(db.String(255), nullable=False)
    usage_time = db.Column(db.String(100), nullable=False)
    
    sold = db.Column( db.Boolean, nullable=False, default=False )
    buyer_id = db.Column( db.Integer, db.ForeignKey("user.id"), nullable=True )

    categories = db.relationship('Category', secondary=product_category, lazy='subquery', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner_name': self.owner.name if self.owner else None,
            'owner_phone': self.owner.phone if self.owner else None,
            'cost': self.cost,
            'post_date': self.post_date.isoformat() if self.post_date else None,
            'quantity': self.quantity,
            'description': self.description,
            'condition': self.condition,
            'pickup_location': self.pickup_location,
            'usage_time': self.usage_time,
            'images': self.image_paths.split(',') if self.image_paths else [],
            'categories': [c.name for c in self.categories] 
        }