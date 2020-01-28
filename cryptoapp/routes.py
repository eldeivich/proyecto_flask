from cryptoapp import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/purchase")
def purchase():
    return render_template("purchase.html")

@app.route("/status")
def status():
    return render_template("status.html")