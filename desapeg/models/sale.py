from datetime import datetime, timezone
from desapeg.extensions import db

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    sold_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    product = db.relationship("Product", backref=db.backref("sales", lazy=True, cascade="all, delete-orphan"))
    buyer = db.relationship("User", backref=db.backref("purchases", lazy=True))

    def __repr__(self):
        return f'<Sale product_id={self.product_id} buyer_id={self.buyer_id} quantity={self.quantity}>'
