from desapeg.extensions import db
from desapeg.models.sale import Sale
from desapeg.models.product_interest import ProductInterest

#Gerenciamento de um produto
# REFATORAÇÃO (Service Layer / Solução de Coupler e SRP):
# Criada uma Camada de Serviço dedicada para isolar a regra de negócio complexa de uma venda.
# Isto evita "Feature Envy" e "Inappropriate Intimacy" dentro do routes.py.
def execute_product_sale(product, buyer_id, quantity_sold):
    if quantity_sold > product.quantity:
        raise ValueError(f"Quantidade solicitada ({quantity_sold}) é maior que a disponível ({product.quantity}).")

    #Atualiza estoque do produto
    product.quantity = max(0, product.quantity - quantity_sold)
    
    #Registra o histórico da venda
    sale = Sale(product_id=product.id, buyer_id=buyer_id, quantity=quantity_sold)
    db.session.add(sale)

    #Atualizações legadas de compatibilidade
    product.buyer_id = buyer_id
    product.sold = True

    #Remove o interesse deste comprador específico
    interest = ProductInterest.query.filter_by(
        product_id=product.id,
        user_id=buyer_id
    ).first()
    
    if interest:
        db.session.delete(interest)