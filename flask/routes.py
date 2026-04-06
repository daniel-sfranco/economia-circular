import json
import os
from flask import Blueprint, jsonify, render_template

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def homepage():
    return render_template("index.html")

@main_routes.route('/api/produtos')
def listar_produtos():

    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_json = os.path.join(current_directory, '..', 'produtos.json')
    
    try:
        with open(path_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return jsonify(dados)
    except FileNotFoundError:
        return jsonify({"erro": "Arquivo não encontrado"}), 404