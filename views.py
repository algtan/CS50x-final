from flask import Flask, redirect, render_template, request, session
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


@app.route("/monthly/", methods=["GET", "POST"])
def monthly():
    # Calculate the user's total monthly payment

    # If request method is POST
    if request.method == "POST":

        # If field is left empty, make the default value zero (.01% for interest rate, 1 year for term)

        # Home Price
        if not request.form.get("home_price"):
            home_price = 0
        else:
            home_price = int(request.form.get("home_price"))
        # Down Payment
        if not request.form.get("down_pmt"):
            down_pmt = 0
        else:
            down_pmt = int(request.form.get("down_pmt"))
        # Interest Rate
        if not request.form.get("int_rate"):
            int_rate = 0.01
        else:
            int_rate = float(request.form.get("int_rate"))
        # Term
        if not request.form.get("term"):
            term = 1
        else:
            term = int(request.form.get("term"))
        # HOA
        if not request.form.get("hoa"):
            hoa = 0
        else:
            hoa = int(request.form.get("hoa"))
        # Mello-roos
        if not request.form.get("melloroos"):
            melloroos = 0
        else:
            melloroos = int(request.form.get("melloroos"))
        # Property Tax
        if not request.form.get("prop_tax"):
            prop_tax = 0
        else:
            prop_tax = int(request.form.get("prop_tax"))   
        # Insurance
        if not request.form.get("ins"):
            ins = 0
        else:
            ins = int(request.form.get("ins"))
        # PMI
        if not request.form.get("pmi"):
            pmi = 0
        else:
            pmi = int(request.form.get("pmi"))

        # Calculate principal of the loan
        P = home_price - down_pmt
        # Calculate the monthly interest rate
        r = int_rate/100/12
        # Calculate the number of payments
        n = term * 12

        monthly_mortgage = P * (r * (1+r)**n) / ((1+r)**n - 1)
        other_expenses = hoa + melloroos + prop_tax/12 + ins/12 + pmi

        total_monthly = monthly_mortgage + other_expenses
    
        # Return the calculated total monthly payment to the user
        return render_template("monthly.html", home_price = home_price, down_pmt = down_pmt, int_rate = int_rate, term = term,
                               hoa = hoa, melloroos = melloroos, prop_tax = prop_tax, ins = ins, pmi = pmi,
                               total_monthly_formatted='${:,.2f}'.format(total_monthly))

    # If the user has not submitted the form, present the form to the user
    else:
        return render_template("monthly.html")