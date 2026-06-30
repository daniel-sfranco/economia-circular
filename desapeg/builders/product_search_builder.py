from desapeg.models.product import Product
from desapeg.models.category import Category
from sqlalchemy import or_

class ProductSearchBuilder:

    def __init__(self):
        self.query = Product.query

    def with_text(self, termo):
        if termo:
            self.query = self.query.filter(
                or_(
                    Product.name.ilike(f"%{termo}%"),
                    Product.description.ilike(f"%{termo}%")
                )
            )
        return self

    def with_product_name(self, nome):
        if nome:
            self.query = self.query.filter(
                Product.name.ilike(f"%{nome}%")
            )
        return self

    def with_seller(self, vendedor):
        if vendedor:
            self.query = self.query.filter(
                Product.seller.ilike(f"%{vendedor}%")
            )
        return self

    def with_price_range(self, preco_min, preco_max):
        if preco_min:
            self.query = self.query.filter(
                Product.cost >= float(preco_min)
            )

        if preco_max:
            self.query = self.query.filter(
                Product.cost <= float(preco_max)
            )

        return self

    def with_categories(self, categorias):
        if categorias:
            self.query = self.query.join(Product.categories).filter(
                Category.name.in_(categorias)
            ).distinct()

        return self

    def build(self):
        return self.query