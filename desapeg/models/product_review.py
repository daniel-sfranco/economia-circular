from desapeg.extensions import db
from datetime import datetime, timezone

class ProductReview(db.Model):
    __table_args__ = (
        db.UniqueConstraint(
            "sale_id",
            name="unique_sale_review"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"), nullable=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    sale = db.relationship("Sale", backref=db.backref("review", uselist=False, cascade="all, delete-orphan"))
    product = db.relationship("Product", backref=db.backref("reviews", lazy=True))