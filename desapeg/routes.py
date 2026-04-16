import json
import os
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from models.product import Product
from forms import ProductForm
from imageHandler import compress_and_save_image

main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def homepage():
    return render_template("index.html")

@main_routes.route('/about')
def aboutpage():
    return render_template("about.html")

@main_routes.route('/product')
def productpage():
    return render_template("product.html")

@main_routes.route('/forms', methods =['GET', 'POST'])
def formspage():
    form = ProductForm()

    if form.validate_on_submit():
        prod_name = form.prod_name.data
        description = form.description.data
        quantity = form.quantity.data
        price = form.price.data
        images = request.files.getlist(form.images.name);

        print(f"Sucesso! Produto: {prod_name} | Preço: {price} | Qtd: {quantity} | Desc: {description}")
        print(f"Imagens enviadas: {images} (total: {len(images)} imagens)")

        return redirect(url_for('main_routes.formspage'))
    
    return render_template("forms.html", form=form)

@main_routes.route('/api/products')
def list_products():
    products = Product.query.all()
    products_dict = [product.to_dict() for product in products]
    return jsonify(products_dict)

@main_routes.route('/api/productInfo/<prod_id>')
def list_info(prod_id):
    product = Product.query.get(prod_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"erro": "Produto não encontrado"}), 404
