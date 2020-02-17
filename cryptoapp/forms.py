from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, IntegerField, DecimalField, FloatField
from wtforms.validators import DataRequired, ValidationError, InputRequired, NumberRange
from wtforms.widgets import Select
from .funciones import cartera


CHOICES = (('EUR', 'Euros'), ('BTC', 'Bitcoin'), ('LTC', 'Litecoin'), ('XRP', 'XRP'), ('XLM', 'Stellar'), ('USDT', 'Tether'), ('ETH', 'Ethereum'), ('EOS', 'EOS'), ('BCH', 'Bitcoin Cash'), ('BNB', 'Binance Coin'), ('TRX', 'Tron'), ('ADA', 'Cardano'), ('BSV', 'Bitcoin SV'))
CRYPTOS = dict(CHOICES)
MONEDAS = {'EUR': 0, 'BTC': 0, 'LTC': 0, 'XRP': 0, 'XLM': 0, 'USDT': 0, 'ETH': 0, 'EOS': 0, 'BCH': 0, 'BNB': 0, 'TRX': 0, 'ADA': 0, 'BSV': 0}

def error_cuantia(form, field):
    if form.cuantia.errors:
        try:
            cuantia = float(form.cuantia.raw_data[0].replace(",","."))
            a=4
        except:
            a=4
        raise ValidationError('Este campo debe ir rellenado con números.')

def error_iguales(form, field):
    if form.convertir_a.data == form.desde.data:
        raise ValidationError('Los campos From y To no deben ser iguales')

def error_euro_no_btc(form, field):
    if form.desde.data == 'EUR' and form.convertir_a.data != 'BTC':
        raise ValidationError('Desde Euros solo se puede convertir a BitCoin')

def error_crypto_no_euro(form, field):
    if form.desde.data != 'BTC' and form.convertir_a.data == 'EUR':
        raise ValidationError('No se puede convertir a euros una crypto que no sea BitCoin')

def cantidad_disponible(form, field):
    disponible = cartera()
    if form.desde.data == 'BTC' and form.convertir_a.data != 'EUR':
        if disponible[0][form.desde.data] < form.cuantia.data:
            raise ValidationError('No Tienes BitCoins suficientes, Realiza una transacción de Euros a BitCoin')
    if form.desde.data != 'EUR':
        if disponible[0][form.desde.data] < form.cuantia.data:
            raise ValidationError('No tienes {} suficientes, Realiza primero una transacción\rde otra moneda en la que tengas credito suficiente a {}.'.format(CRYPTOS[form.desde.data], CRYPTOS[form.desde.data]))
    if disponible == True:
        raise ValidationError('Un error con la base de datos ha ocurrido, por favor inténtelo en unos minutos.')

class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
                a=4
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid float value'))

class CryptoForm(FlaskForm):
    
    desde = SelectField('From', validators=[DataRequired(), error_iguales, error_euro_no_btc], choices=CHOICES, id="state")
    convertir_a = SelectField('To', validators=[DataRequired(), error_iguales, error_crypto_no_euro], choices=CHOICES)
    cuantia = MyFloatField('Q', validators=[InputRequired(), error_cuantia, cantidad_disponible, NumberRange(min=0.00001, max=99999999)])
    
    calc = SubmitField('Calcular')
    
    ok = SubmitField('Ok')
    
    
    