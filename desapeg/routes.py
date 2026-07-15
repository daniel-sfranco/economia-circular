import json
import os
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, current_app

from desapeg.builders import ProductSearchBuilder
from desapeg.models.category import Category
from .models.product import Product
from .models.user import User
from .models.product_interest import ProductInterest
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

@main_routes.route('/evaluate')
def evaluatepage():
    product_id = request.args.get('product_id')
    buyer_id = request.args.get('buyer_id')
    seller_id = request.args.get('seller_id')
    return render_template(
        "evaluate.html",
        product_id=product_id,
        buyer_id=buyer_id,
        seller_id=seller_id
    )

@main_routes.route('/compras')
def compraspage():
    user_id = 1

    interests = (
        db.session.query(ProductInterest)
        .filter(ProductInterest.user_id == user_id)
        .order_by(ProductInterest.contact_date.desc())
        .all()
    )

    compras = []
    for interest in interests:
        product = interest.product
        if not product:
            continue

        seller = User.query.get(product.user_id)
        can_evaluate = product.sold and product.buyer_id == user_id

        compras.append({
            "product_id": product.id,
            "product_name": product.name,
            "seller_name": seller.name if seller else "",
            "price": product.cost,
            "buyer_id": user_id,
            "seller_id": product.user_id,
            "status": "Vendido" if product.sold else "Interessado",
            "can_evaluate": can_evaluate
        })

    return render_template("compras.html", compras=compras)

@main_routes.route('/myproducts')
def myproducts():
    meus_produtos = Product.query.filter_by(user_id=1).all()
    
    return render_template(
        "myproducts.html", 
        produtos=meus_produtos,
        termo="Meus Anúncios"
    )

@main_routes.route('/editproduct/<int:prod_id>')
def edit_product_page(prod_id):
    produto = Product.query.get_or_404(prod_id)

    interesses = (
        db.session.query(ProductInterest.user_id, User.name)
        .join(User, ProductInterest.user_id == User.id)
        .filter(ProductInterest.product_id == produto.id)
        .all()
    )

    buyer = User.query.get(produto.buyer_id) if produto.buyer_id else None

    return render_template(
        "editproduct.html",
        produto=produto,
        interesses=interesses,
        buyer_name=buyer.name if buyer else None
    )

@main_routes.route('/api/product/<int:prod_id>/sell', methods=['POST'])
def mark_product_sold(prod_id):
    produto = Product.query.get_or_404(prod_id)
    data = request.get_json(silent=True) or {}
    buyer_id = data.get('buyer_id')

    if buyer_id is None:
        return jsonify({"error": "Selecione um comprador."}), 400

    buyer = User.query.get(int(buyer_id))
    if not buyer:
        return jsonify({"error": "Usuário não encontrado."}), 404

    produto.sold = True
    produto.buyer_id = buyer.id
    db.session.commit()

    return jsonify({
        "success": True,
        "buyer_id": buyer.id,
        "buyer_name": buyer.name
    })

@main_routes.route('/api/product/<int:prod_id>', methods=['PUT'])
def update_product(prod_id):
    produto = Product.query.get_or_404(prod_id)

    form = ProductForm(meta={'csrf': False})

    # Remove o DataRequired do campo de imagens APENAS para a edição
    form.images.validators = [v for v in form.images.validators if type(v).__name__ != 'DataRequired']

    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    produto.name = form.name.data
    produto.description = form.description.data
    produto.condition = form.condition.data
    produto.cost = float(form.cost.data)
    produto.quantity = int(form.quantity.data)
    produto.usage_time = form.usage_time.data
    produto.pickup_location = form.pickup_location.data

    categorias_str = form.categories.data
    nomes_categorias = [
        nome.strip()
        for nome in categorias_str.split(",")
        if nome.strip()
    ]

    categorias_db = Category.query.filter(
        Category.name.in_(nomes_categorias)
    ).all()
    produto.categories = categorias_db

    novas_imagens = request.files.getlist(form.images.name)

    # Só altera as imagens no banco e no disco SE o usuário enviou novos arquivos
    if novas_imagens and novas_imagens[0].filename != "":
        upload_path = os.path.join(
            current_app.root_path,
            "static",
            "uploads"
        )

        imagens_antigas = (
            produto.image_paths.split(",")
            if produto.image_paths
            else []
        )

        for nome_imagem in imagens_antigas:
            caminho = os.path.join(upload_path, nome_imagem)
            if os.path.exists(caminho):
                os.remove(caminho)

        novos_nomes = []

        for imagem in novas_imagens:
            nome_salvo = compress_and_save_image(
                imagem,
                upload_path
            )
            novos_nomes.append(nome_salvo)

        produto.image_paths = ",".join(novos_nomes)

    db.session.commit()

    return jsonify({
        "success": True
    })

@main_routes.route('/api/product/<int:prod_id>', methods=['DELETE'])
def delete_product(prod_id):
    produto = Product.query.get_or_404(prod_id)

    upload_path = os.path.join(
    current_app.root_path,
    'static',
    'uploads'
    )

    imagens = (
        produto.image_paths.split(',')
        if produto.image_paths
        else []
    )

    for imagem in imagens:
        caminho = os.path.join(upload_path, imagem)

        if os.path.exists(caminho):
            os.remove(caminho)

    db.session.delete(produto)
    db.session.commit()

    return jsonify({
        "success": True
    })

@main_routes.route('/forms', methods =['GET', 'POST'])
def formspage():
    form = ProductForm()

    if form.validate_on_submit():
        prod_name = form.name.data
        description = form.description.data
        quantity = form.quantity.data
        price = form.cost.data
        condition=form.condition.data
        usage_time=form.usage_time.data
        pickup_location=form.pickup_location.data
        
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
            user_id=1, # depois ligar o usuário de verdade ao produto adicionado
            cost=price,
            quantity=quantity,
            description=description,
            image_paths=images_str,
            categories=categorias_db,
            condition=condition,
            usage_time=usage_time,
            pickup_location=pickup_location
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
    nome_produto = request.args.get("produto", "")
    vendedor = request.args.get("vendedor", "")
    pickup_location = request.args.get("local", "")
    preco_min = request.args.get("preco_min", 0, type=int)
    preco_max = request.args.get("preco_max", 5000, type=int)

    categorias = request.args.getlist("categoria")

    produtos = (
        ProductSearchBuilder()
            .with_text(termo)
            .with_product_name(nome_produto)
            .with_owner(vendedor)
            .with_pickup_location(pickup_location)
            .with_price_range(preco_min, preco_max)
            .with_categories(categorias)
            .build()
            .all()
    )

    return render_template(
        "search_results.html",
        produtos=produtos,
        termo=termo,
        nome_produto=nome_produto,
        vendedor=vendedor,
        pickup_location=pickup_location,
        preco_min=preco_min,
        preco_max=preco_max,
        categorias_selecionadas=categorias
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

@main_routes.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")