from cryptoapp import app
from flask import render_template, request, redirect, url_for
import requests
from requests import Request, Session, ConnectionError, Timeout, TooManyRedirects
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from flask_wtf import FlaskForm
from cryptoapp.forms import CryptoForm
from .funciones import inversion, tablaCryptos, consultaApi, tablaCryptos, cartera
import json
import sqlite3
from sqlite3 import OperationalError
import time

BASE_DATOS = './data/data.db'
API_KEY= app.config['API_KEY']
cartera = cartera()
tablaCryptos()


@app.route("/", methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    query = "SELECT * from movements;"
    try:
        filas = cursor.execute(query)
    except OperationalError as o:
        return render_template("index.html", o=o)

    listado = []
    valorUnit = []
    for fila in filas:
        fila = list(fila)
        valorUnit = fila[4] / fila[6]
        #valorUnit = round((fila[4] / fila[6]), 5)
        fila.append(valorUnit)
        fila = tuple(fila)
        listado.append(fila)
    
    conn.close()

    return render_template("index.html", listado = listado)

@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    form = CryptoForm(request.form)

    if request.method == 'GET':
        return render_template("purchase.html", form = form, cartera=cartera)

    if form.calc.data:
        if form.validate():
            desde = request.form.get('desde')
            convertir_a = request.form.get('convertir_a')
            cuantia = form.cuantia.data

            consulta = consultaApi(desde, convertir_a, cuantia)

            if consulta == False:
                mensaje = 'Error en la consulta a la api, vuelva a intentarlo en unos minutos.'
                return render_template("purchase.html", form=form, mensaje=mensaje, cartera=cartera)

            qcuantity = consulta['data']['quote'][convertir_a]['price']
            qcuantity_unitario = (cuantia / qcuantity)
            #qcuantity_unitario = round((cuantia / qcuantity), 5)

            return render_template("purchase.html", form=form, qcuantity = qcuantity, qcuantity_unitario = qcuantity_unitario, cartera=cartera)
        else:
            return render_template("purchase.html", form=form, cartera=cartera)
    elif form.ok.data:
        desde = request.form.get('desde')
        convertir_a = request.form.get('convertir_a')
        cuantia = form.cuantia.data
        qcuantity = float(request.form.get('qcuantityh'))
        qcuantity_unitario = float(cuantia / qcuantity)
        #qcuantity_unitario = float(round((cuantia / qcuantity), 5))
        hora = time.strftime('%H:%M:%S')
        fecha = time.strftime('%d/%m/%Y')

        conn = sqlite3.connect(BASE_DATOS)
        cursor = conn.cursor()
        query = "INSERT into movements (date, time, from_currency, from_quantity, to_currency, to_quantity) values(?, ?, ?, ?, ?, ?);"
        try:
            cursor.execute(query, (fecha, hora, desde, cuantia, convertir_a, qcuantity))
        except OperationalError as o:
            return render_template("purchase.html", form=form ,o=o, cartera=cartera)

        conn.commit()
        conn.close()

        return redirect(url_for("index"))




@app.route("/status")
def status():
    disponible = inversion()
    if disponible == True:
        return render_template("status.html", mensaje="Error con la base de datos, Por favor inténtelo de nuevo en unos minutos.")
    elif disponible == False:
        return render_template("status.html", mensaje="Error en la consulta a la api, vuelva a intentarlo en unos minutos.")
    euros_invertidos = disponible[0]
    #euros_invertidos = round(disponible[0], 5)
    valor_actual = disponible[1]
    #valor_actual = round(disponible[1], 5)

    return render_template("status.html", euros_invertidos=euros_invertidos, valor_actual=valor_actual)