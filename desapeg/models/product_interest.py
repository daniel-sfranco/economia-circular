from datetime import datetime, timezone
from desapeg.extensions import db

class ProductInterest(db.Model):


    __table_args__ = (
        db.UniqueConstraint(
            "product_id",
            "user_id",
            name="unique_product_interest"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column( db.Integer, db.ForeignKey("product.id"), nullable=False )
    user_id = db.Column( db.Integer, db.ForeignKey("user.id"), nullable=False )
    contact_date = db.Column( db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) )
    product = db.relationship( "Product", backref=db.backref( "interested_users", lazy=True, cascade="all, delete-orphan") )
    user = db.relationship( "User", backref=db.backref("product_interests", lazy=True) )