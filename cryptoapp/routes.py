from cryptoapp import app
from flask import render_template, request, redirect, url_for
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout
from cryptoapp.forms import CryptoForm
from .funciones import inversion
import json
import sqlite3
import time

BASE_DATOS = './data/data.db'
API_KEY= app.config['API_KEY']

def tablaCryptos():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

    parameters = {
        'symbol' : 'BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX'
    }

    headers = {
        'Accepts' : 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    

    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    query = "INSERT into cryptos (id, symbol, name) values(?, ?, ?);"
    for insert in data['data']:
        cursor.execute(query, (insert['id'], insert['symbol'], insert['name']))
    conn.commit()
    conn.close()

def consultaApi(desde, convertir_a, cuantia):
    url_consulta = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
    parametros = {'amount': cuantia, 'symbol': desde, 'convert': convertir_a}
    parametros_unidad = {'amount': 1, 'symbol': desde, 'convert': convertir_a}

    headers = {
        'Accepts' : 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    session = Session()
    session.headers.update(headers)
    
    try:
        respuesta = session.get(url_consulta, params=parametros)
        respuesta_unidad = session.get(url_consulta,params=parametros_unidad)
        consulta = json.loads(respuesta.text)
        consulta_unidad = json.loads(respuesta_unidad.text)
    except(ConnectionError, timeout, TooManyRedirects) as e2:
        print(e2)

    return consulta, consulta_unidad

@app.route("/", methods=['GET', 'POST'])
def index():

    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    query = "SELECT * from movements;"
    filas = cursor.execute(query)
    
    listado = []
    valorUnit = []
    for fila in filas:
        fila = list(fila)
        '''
        unidad = consultaApi(fila[3], fila[5], 1)
        '''
        valorUnit = round((fila[4] / fila[6]), 5)
        '''
        valorUnit = unidad[0]['data']['quote'][fila[5]]['price']
        '''
        fila.append(valorUnit)
        fila = tuple(fila)
        listado.append(fila)
    
    conn.close()

    return render_template("index.html", listado = listado)

@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    form = CryptoForm(request.form)

    if request.method == 'GET':
        return render_template("purchase.html", form = form)

    if form.calc.data:
        if form.validate():
            desde = request.form.get('desde')
            convertir_a = request.form.get('convertir_a')
            cuantia = int(request.form.get('cuantia'))

            url_consulta = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
            parametros = {'amount': cuantia, 'symbol': desde, 'convert': convertir_a}
            parametros_unidad = {'amount': 1, 'symbol': desde, 'convert': convertir_a}

            headers = {
                'Accepts' : 'application/json',
                'X-CMC_PRO_API_KEY': API_KEY
            }

            session = Session()
            session.headers.update(headers)
            
            try:
                respuesta = session.get(url_consulta, params=parametros)
                respuesta_unidad = session.get(url_consulta,params=parametros_unidad)
                consulta = json.loads(respuesta.text)
                consulta_unidad = json.loads(respuesta_unidad.text)
            except(ConnectionError, timeout, TooManyRedirects) as e2:
                print(e2)

            qcuantity = round(consulta['data']['quote'][convertir_a]['price'], 5)
            qcuantity_unitario = round((cuantia / qcuantity), 5)

            return render_template("purchase.html", form=form, qcuantity = qcuantity, qcuantity_unitario = qcuantity_unitario)
        else:
            return render_template("purchase.html", form=form)
    elif form.ok.data:
        desde = request.form.get('desde')
        convertir_a = request.form.get('convertir_a')
        cuantia = int(request.form.get('cuantia'))
        qcuantity = float(request.form.get('qcuantityh'))
        qcuantity_unitario = float(round((cuantia / qcuantity), 5))
        hora = time.strftime('%H:%M:%S')
        fecha = time.strftime('%d/%m/%Y')

        conn = sqlite3.connect(BASE_DATOS)
        cursor = conn.cursor()
        query = "INSERT into movements (date, time, from_currency, from_quantity, to_currency, to_quantity) values(?, ?, ?, ?, ?, ?);"
        cursor.execute(query, (fecha, hora, desde, cuantia, convertir_a, qcuantity))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))




@app.route("/status")
def status():
    disponible = inversion()
    euros_invertidos = round(disponible[0], 5)
    valor_actual = round(disponible[1], 5)

    return render_template("status.html", euros_invertidos=euros_invertidos, valor_actual=valor_actual)