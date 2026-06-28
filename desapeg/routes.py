import json
import os
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, current_app

from desapeg.models.category import Category
from .models.product import Product
from .forms import ProductForm
from .imageHandler import compress_and_save_image
from .extensions import db
from sqlalchemy import or_
from datetime import datetime
from flask import jsonify

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
        
        images = request.files.getlist(form.images.name)
        saved_image_names = []
        
        categorias_str = form.categories.data
        cat_names = [nome.strip() for nome in categorias_str.split(',') if nome.strip()]
        categorias_db = Category.query.filter(Category.name.in_(cat_names)).all()
        
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_path, exist_ok=True)

        for file in images:
            if file and file.filename != '':
                saved_filename = compress_and_save_image(file, upload_path)
                saved_image_names.append(saved_filename)

        images_str = ",".join(saved_image_names)

        # Criação do objeto
        new_product = Product(
            name=prod_name,
            seller="Usuário de Teste", # depois ligar o usuário de verdade ao produto adicionado
            cost=price,
            quantity=quantity,
            description=description,
            image_paths=images_str,
            categories=categorias_db
        )

        try:
            db.session.add(new_product)
            db.session.commit()
            print(f"Sucesso! Produto {prod_name} salvo no banco com {len(saved_image_names)} imagens!")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar no banco: {e}")

        return redirect(url_for('main_routes.formspage'))
    
    return render_template("forms.html", form=form)

@main_routes.route('/api/products')
def list_products():
    products = Product.query.all()
    products_dict = [product.to_dict() for product in products]
    return jsonify(products_dict)

@main_routes.route("/search")
def search_page():

    termo = request.args.get("q", "")

    produtos = Product.query.filter(
        or_(
            Product.name.ilike(f"%{termo}%"),
            Product.description.ilike(f"%{termo}%"),
        )
    ).all()

    return render_template(
        "search_results.html",
        produtos=produtos,
        termo=termo
    )

@main_routes.app_template_filter('elapsed_time')
def format_elapsed_time(post_date):
    now = datetime.now()
    elapsed_seconds = int((now - post_date).total_seconds())

    if elapsed_seconds < 60:
        return "agora mesmo"

    intervals = [
        ("ano", 31536000),
        ("mês", 2592000),
        ("dia", 86400),
        ("hora", 3600),
        ("minuto", 60)
    ]

    for nome, segundos in intervals:
        quantidade = elapsed_seconds // segundos

        if quantidade >= 1:
            unidade = nome

            if quantidade > 1:
                unidade = "meses" if unidade == "mês" else unidade + "s"

            return f"há {quantidade} {unidade}"

@main_routes.route('/api/productInfo/<prod_id>')
def list_info(prod_id):
    product = Product.query.get(prod_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"erro": "Produto não encontrado"}), 404

@main_routes.route("/api/search")
def api_search():
    termo = request.args.get("q", "")
    
    if not termo:
        return jsonify([])

    produtos = Product.query.filter(
        or_(
            Product.name.ilike(f"%{termo}%"),
            Product.description.ilike(f"%{termo}%"),
        )
    ).limit(5).all()

    return jsonify([produto.to_dict() for produto in produtos])

@main_routes.route('/api/categorias')
def api_categorias():
    categorias = Category.query.all()
    nomes_categorias = [c.name for c in categorias] 
    return jsonify(nomes_categorias)

@main_routes.route('/api/similarProducts/<int:prod_id>')
def api_similar_products(prod_id):
    product = Product.query.get(prod_id)
    
    if not product or not product.categories:
        return jsonify([])

    category_ids = [c.id for c in product.categories]

    similar_products = Product.query.join(Product.categories)\
        .filter(Category.id.in_(category_ids))\
        .filter(Product.id != prod_id)\
        .distinct()\
        .limit(10)\
        .all()

    return jsonify([p.to_dict() for p in similar_products])