from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError

def max_text_len(max_len):
    def _max_text_len(form, field):
        if field.data and len(field.data) > max_len:
            raise ValidationError(f'O texto não pode ter mais de {max_len} caracteres')
    return _max_text_len

class ReviewForm(FlaskForm):
    # O campo de nota (rating) recebe de 1 a 5
    rating = IntegerField('Sua nota', validators=[
        DataRequired(message="Por favor, selecione uma nota de 1 a 5 estrelas."),
        NumberRange(min=1, max=5, message="A nota deve ser entre 1 e 5 estrelas.")
    ])
    
    # O comentário é opcional, mas limitado a 80 caracteres conforme o banco de dados
    comment = TextAreaField('Comentário', validators=[
        Optional(),
        max_text_len(80)
    ])
    
    product_id = HiddenField('Product ID')
    buyer_id = HiddenField('Buyer ID')
    seller_id = HiddenField('Seller ID')
    sale_id = HiddenField('Sale ID')
    
    submit = SubmitField('Enviar avaliação')