from cryptoapp import app
from flask import render_template, request, redirect, url_for
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout
import json
import sqlite3

BASE_DATOS = './data/data.db'

def tablaCryptos():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

    parameters = {
        'symbol' : 'BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX'
    }

    headers = {
        'Accepts' : 'application/json',
        'X-CMC_PRO_API_KEY': 'a149b700-87b4-4f94-8c08-ea7d6bcdc9df'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    

    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    query = "INSERT into cryptos (id, symbol, name) values(?, ?, ?);"
    for insert in data['data']:
        cursor.execute(query, (insert['id'], insert['symbol'], insert['name']))
    conn.commit()
    conn.close()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    if request.method == 'GET':
        print('estoy en GET')
        return render_template("purchase.html")
    
    desde = request.values.get('from')
    convertir_a = request.values.get('to')
    cuantia = int(request.values.get('q'))

    url_consulta = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
    parametros = {'amount': cuantia, 'symbol': desde, 'convert': convertir_a}
    parametros_unidad = {'amount': 1, 'symbol': desde, 'convert': convertir_a}

    headers = {
        'Accepts' : 'application/json',
        'X-CMC_PRO_API_KEY': 'a149b700-87b4-4f94-8c08-ea7d6bcdc9df'
    }

    session = Session()
    session.headers.update(headers)
    
    try:
        respuesta = session.get(url_consulta, params=parametros)
        respuesta_unidad = session.get(url_consulta,params=parametros_unidad)
        consulta = json.loads(respuesta.text)
        consulta_unidad = json.loads(respuesta_unidad.text)
        print('----------------------------------------------------')
        print(consulta)
        print('----------------------------------------------------')
        print(consulta_unidad)
    except(ConnectionError, timeout, TooManyRedirects) as e2:
        print(e2)

    print('method:', request.method)
    print('parameters:', request.values)

    qcuantity = consulta['data']['quote'][convertir_a]['price']
    qcuantity_unitario = consulta_unidad['data']['quote'][convertir_a]['price']
    print('la cantidad es: ', qcuantity, 'Y el precio unitario: ', qcuantity_unitario)

    return render_template("purchase.html", qcuantity = qcuantity, qcuantity_unitario = qcuantity_unitario)
    
    

@app.route("/status")
def status():
    return render_template("status.html")