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

BASE_DATOS = './datas/{}'.format(app.config['DB_FILE'])
API_KEY= app.config['API_KEY']
creatabla = tablaCryptos()

@app.route("/", methods=['GET', 'POST'])
def index():
    
    if creatabla == False:
        return render_template("index.html", creatabla=creatabla)
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
        valorUnit = '{:,.5f}'.format(valorUnit).replace(",", "@").replace(".", ",").replace("@", ".")
        fila.append(valorUnit)
        valor4 = fila.pop(4)
        valor4 = '{:,.5f}'.format(valor4).replace(",", "@").replace(".", ",").replace("@", ".")
        fila.insert(4, valor4)
        valor6 = fila.pop(6)
        valor6 = '{:,.5f}'.format(valor6).replace(",", "@").replace(".", ",").replace("@", ".")
        fila.insert(6, valor6)
        fila = tuple(fila)
        listado.append(fila)
    
    conn.close()

    return render_template("index.html", listado = listado)

@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    form = CryptoForm(request.form)
    carteras = cartera()
    
    if carteras != True:
        for valores in carteras[0]:
            if carteras[0][valores] == 0:
                continue
            carteras[0][valores] = '{:,.5f}'.format(carteras[0][valores]).replace(",", "@").replace(".", ",").replace("@", ".")

    if request.method == 'GET':
        return render_template("purchase.html", form = form, carteras=carteras)

    if form.calc.data:
        if form.validate():
            desde = request.form.get('desde')
            convertir_a = request.form.get('convertir_a')
            cuantia = form.cuantia.data

            consulta = consultaApi(desde, convertir_a, cuantia)

            if consulta == False:
                mensaje = 'Error en la consulta a la api, vuelva a intentarlo en unos minutos.'
                return render_template("purchase.html", form=form, mensaje=mensaje, carteras=carteras)

            qcuantity = consulta['data']['quote'][convertir_a]['price']
            qcuantityformat = '{:,.5f}'.format(qcuantity).replace(",", "@").replace(".", ",").replace("@", ".")
            qcuantity_unitario = (cuantia / qcuantity)
            qcuantity_unitarioformat = '{:,.5f}'.format(qcuantity_unitario).replace(",", "@").replace(".", ",").replace("@", ".")
            

            return render_template("purchase.html", form=form, qcuantity = qcuantity, qcuantityformat=qcuantityformat, qcuantity_unitario = qcuantity_unitario, qcuantity_unitarioformat=qcuantity_unitarioformat, carteras=carteras)
        else:
            return render_template("purchase.html", form=form, carteras=carteras)
    elif form.ok.data:
        desde = request.form.get('desde')
        convertir_a = request.form.get('convertir_a')
        cuantia = form.cuantia.data
        qcuantity = float(request.form.get('qcuantityh'))
        qcuantityformat = '{:,.5f}'.format(qcuantity).replace(",", "@").replace(".", ",").replace("@", ".")
        qcuantity_unitario = float(cuantia / qcuantity)
        qcuantity_unitarioformat = '{:,.5f}'.format(qcuantity_unitario).replace(",", "@").replace(".", ",").replace("@", ".")
        hora = time.strftime('%H:%M:%S')
        fecha = time.strftime('%d/%m/%Y')

        conn = sqlite3.connect(BASE_DATOS)
        cursor = conn.cursor()
        query = "INSERT into movements (date, time, from_currency, from_quantity, to_currency, to_quantity) values(?, ?, ?, ?, ?, ?);"
        try:
            cursor.execute(query, (fecha, hora, desde, cuantia, convertir_a, qcuantity))
        except:
            o=1
            return render_template("purchase.html", form=form ,o=o, carteras=carteras,qcuantity=qcuantity,qcuantity_unitario=qcuantity_unitario ,qcuantityformat=qcuantityformat, qcuantity_unitarioformat=qcuantity_unitarioformat)

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
    euros_invertidos = '{:,.5f}'.format(euros_invertidos).replace(",", "@").replace(".", ",").replace("@", ".")  
    valor_actual = disponible[1]
    valor_actual = '{:,.5f}'.format(valor_actual).replace(",", "@").replace(".", ",").replace("@", ".")

    return render_template("status.html", euros_invertidos=euros_invertidos, valor_actual=valor_actual)