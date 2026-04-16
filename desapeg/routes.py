import json
import os
from flask import Blueprint, jsonify, render_template
from models.product import Product
from models.user import User
from extensions import db

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

@main_routes.route('/api/products')
def list_products():
    results = db.session.query(
        Product.Product_ID,
        Product.Name,
        Product.Post_Date,
        User.Name.label('seller_name')
    ).join(
        User, Product.User_ID == User.User_ID
    ).order_by(
        Product.Post_Date.desc()
    ).limit(10).all()

    products_list = []
    for row in results:
        product_data = {
            "id": row.Product_ID,
            "name": row.Name,
            "post_date": row.Post_Date.isoformat() + "Z",
            "seller_name": row.seller_name
        }

        products_list.append(product_data)

    return jsonify(products_list)


@main_routes.route('/api/productInfo/<prod_id>')
def list_info(prod_id):
    result = db.session.query(
        Product.Product_ID,
        Product.Name,
        Product.Price,
        Product.Post_Date,
        Product.Quantity,
        Product.Description,
        User.Name.label('seller_name')
    ).join(
        User, Product.User_ID == User.User_ID
    ).filter(
        Product.Product_ID == prod_id 
    ).first()

    if result:
        product_data = {
            "product_id": result.Product_ID,
            "product_name": result.Name,
            "seller": result.seller_name,
            "cost": result.Price,
            "post_date": result.Post_Date.isoformat() + "Z",
            "quantity": result.Quantity,
            "description": result.Description
        }
        return jsonify(product_data)
    
    return jsonify({"erro": "Produto não encontrado"}), 404
