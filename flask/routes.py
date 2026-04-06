import json
import os
from flask import Blueprint, jsonify, render_template

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

    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_json = os.path.join(current_directory, '..', 'fakeDB/produtos.json')
    
    try:
        with open(path_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"erro": "Arquivo não encontrado"}), 404


@main_routes.route('/api/productInfo/<prod_id>')
def list_info(prod_id):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_json = os.path.join(current_directory, '..', 'fakeDB', 'individualProducts', f'produto{prod_id}.json')

    try:
        with open(path_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"erro": "Arquivo não encontrado"}), 404