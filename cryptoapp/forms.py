from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, HiddenField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import Select

def error_cuantia(form, field):
    if form.cuantia.errors:
        raise ValidationError('Este campo debe ir rellenado con números.')

class CryptoForm(FlaskForm):
    desde = SelectField('From', validators=[DataRequired()], choices=[('EUR', 'Euros'), ('BTC', 'Bitcoin'), ('LTC', 'Litecoin'), ('XRP', 'XRP'), ('XLM', 'Stellar'), ('USDT', 'Tether'), ('ETH', 'Ethereum'), ('EOS', 'EOS'), ('BCH', 'Bitcoin Cash'), ('BNB', 'Binance Coin'), ('TRX', 'Tron'), ('ADA', 'Cardano'), ('BSV', 'Bitcoin SV')])
    convertir_a = SelectField('To', validators=[DataRequired()], choices=[('EUR', 'Euros'), ('BTC', 'Bitcoin'), ('LTC', 'Litecoin'), ('XRP', 'XRP'), ('XLM', 'Stellar'), ('USDT', 'Tether'), ('ETH', 'Ethereum'), ('EOS', 'EOS'), ('BCH', 'Bitcoin Cash'), ('BNB', 'Binance Coin'), ('TRX', 'Tron'), ('ADA', 'Cardano'), ('BSV', 'Bitcoin SV')])
    cuantia = IntegerField('Q', validators=[DataRequired(), error_cuantia])

    calc = SubmitField('Calcular')

    ok = SubmitField('Ok')
    
    
    