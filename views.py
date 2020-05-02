from flask import Flask
from flask import render_template
from datetime import datetime
from . import app

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/amortization/")
def amortization():
    return render_template("amortization.html")
    

@app.route("/qualification/")
def qualification():
    return render_template("qualification.html")


@app.route("/monthly/")
def monthly():
    return render_template("monthly.html")