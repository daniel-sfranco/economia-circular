from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError

#validação customizada para máximo de arquivos, máximo de casas decimais do preço e comprimento máximo dos textos.
def max_files(max_uploads):
    def _max_files(form, field):
        if (field.data != None):
            files = [f for f in field.data if f and f.filename]
        if len(files) > max_uploads:
            raise ValidationError(f'Você pode enviar no máximo {max_uploads} imagens.')
    return _max_files
def max_decimal_places(max_places):
    def _max_decimal_places(form, field):
        if field.raw_data and field.raw_data[0]:
            value_str = field.raw_data[0].replace(',', '.')
            if '.' in value_str:
                decimal_part = value_str.split('.')[1]
                if len(decimal_part) > max_places:
                    raise ValidationError(f'O preço deve ter no máximo {max_places} casas decimais.')
    return _max_decimal_places
def max_text_len(max_len):
    def _max_text_len(form, field):
        if len(field.data) > max_len:
            raise ValidationError(f'O texto não pode ter mais de {max_len} caracteres')
    return _max_text_len
        

class ProductForm(FlaskForm):
    prod_name = StringField('Nome do Produto', validators=[
        DataRequired(message="O nome do produto é obrigatório."),
        max_text_len(50)
    ])
    
    description = TextAreaField('Descrição do Produto', validators=[
        DataRequired(message="A descrição é obrigatória."),
        max_text_len(5000)
    ])
    
    price = DecimalField('Preço do Produto (R$)', places = 2, validators=[
        DataRequired(message="O preço é obrigatório. Se seu produto é uma DOAÇÃO, coloque o preço como 0"),
        NumberRange(min=0.0, message="O preço não pode ser negativo."),
        NumberRange(max=10000.0, message="O preço não pode ser mais de 10 mil reais."),
        max_decimal_places(2)
    ])
    
    quantity = IntegerField('Quantidade Disponível', validators=[
        DataRequired(message="A quantidade é obrigatória."),
        NumberRange(min=0, message="A quantidade não pode ser negativa."),
        NumberRange(max=50, message="A quantidade não pode passar de 50 produtos.")
    ])
    
    images = MultipleFileField('Imagens do Produto', validators=[
        DataRequired(message="é necessário enviar pelo menos UM arquivo de imagem."),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens (JPG, PNG, JPEG) são permitidas.'),
        max_files(5)
    ])
    
    submit = SubmitField('Cadastrar Produto')