from extensions import db

class Product(db.Model):
    __tablename__ = 'product'

    Product_ID = db.Column('product_id', db.Integer, primary_key=True)
    Name = db.Column('name', db.String(30))
    Description = db.Column('description', db.String(500))
    Price = db.Column('price', db.Float)
    Post_Date = db.Column('post_date', db.DateTime)
    Quantity = db.Column('quantity', db.Integer)
    
    User_ID = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'))

    def to_dict(self):
        return {
            "id": self.Product_ID,
            "name": self.Name,
            "description": self.Description,
            "price": self.Price,
            "quantity": self.Quantity
        }