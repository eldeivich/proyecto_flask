from cryptoapp import app
import sqlite3
from requests import Request, Session
import json

BASE_DATOS = './data/data.db'
MONEDAS = {'EUR': 0, 'BTC': 0, 'LTC': 0, 'XRP': 0, 'XLM': 0, 'USDT': 0, 'ETH': 0, 'EOS': 0, 'BCH': 0, 'BNB': 0, 'TRX': 0, 'ADA': 0, 'BSV': 0}
API_KEY= app.config['API_KEY']

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

def cartera():
    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    query = "SELECT * from movements;"
    filas = cursor.execute(query)
    euros_invertidos = 0

    for fila in filas:
        if fila[3] == 'EUR' and fila[5] == 'BTC':
            MONEDAS['BTC'] += fila[6]
            euros_invertidos += fila[4]
        if fila[3] == 'BTC' and fila[5] == 'EUR':
            MONEDAS['BTC'] -= fila[4]
            euros_invertidos -= fila[6]
        if fila[3] == 'BTC' and fila[5] != 'EUR':
            MONEDAS['BTC'] -= fila[4]
            MONEDAS[fila[5]] += fila[6]
        if fila[3] != 'BTC' and fila[3] != 'EUR':
            MONEDAS[fila[3]] -= fila[4]
            MONEDAS[fila[5]] += fila[6]

    conn.close()

    return MONEDAS, euros_invertidos

def inversion():
    MONEDAS = cartera()
    euros_invertidos = MONEDAS[1]
    valor_actual = 0

    for clave, valor in MONEDAS[0].items():
        if clave == 'EUR' or valor == 0:
            pass
        else:
            conversion = consultaApi(clave, 'EUR', valor)
            valor_actual += conversion[0]['data']['quote']['EUR']['price']

        '''
        if fila[3] == 'BTC' and fila[5] == 'EUR':
            conversion = consultaApi(clave, 'EUR', MONEDAS[clave])
            MONEDAS[fila[3]] -= fila[4] 
            MONEDAS['EUR'] += conversion[0]['data']['quote']['EUR']['price']
        
            pass
    
            conversion = consultaApi('BTC', 'EUR', fila[4])
        '''

    return euros_invertidos, valor_actual