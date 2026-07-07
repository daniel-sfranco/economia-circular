from desapeg.extensions import db
from desapeg.models.category import Category # Supondo que você criou a model

def seed_categories():
    categorias = [
        "Móveis",
        "Eletrodomésticos",
        "Utensílios",
        "Cama, Mesa e Banho",
        "Eletrônicos e Informática",
        "Livros e Materiais Acadêmicos",
        "Papelaria",
        "Roupas",
        "Transporte/Mobilidade",
        "Jogos",
        "Limpeza",
        "Outros"
    ]

    for nome in categorias:
        # Verifica se já não existe para evitar duplicatas em re-seeds
        if not Category.query.filter_by(name=nome).first():
            db.session.add(Category(name=nome))
            
    db.session.commit()
    print("Categorias inseridas com sucesso.")