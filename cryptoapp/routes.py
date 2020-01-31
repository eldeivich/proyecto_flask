from cryptoapp import app
from flask import render_template
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout
import json

@app.route("/", methods=['GET', 'POST'])
def index():
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

    return render_template("index.html")

@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
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

    return render_template("purchase.html")

@app.route("/status")
def status():
    return render_template("status.html")