from flask import Flask, redirect, render_template, request, session
from datetime import datetime
from . import app

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/amortization/", methods=["GET", "POST"])
def amortization():
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
        
        # Calculate principal of the loan
        P = home_price - down_pmt
        # Calculate the monthly interest rate
        r = int_rate/100/12
        # Calculate the number of payments
        n = term * 12

        # Calculate amortizaiton data
        monthly_mortgage = P * (r * (1+r)**n) / ((1+r)**n - 1)
        
        # Create list of dictionaries for amortization data
        rows = []
        pmt_no = []
        interest = []
        principal = []
        Pr = []
        
        # For loop to go through each payment's information
        for i in range(n):
            if i == 0:
                pmt_no.append(1)
                interest.append(P * r)
                principal.append(monthly_mortgage - interest[i])
                Pr.append(P - principal[i])
            else:
                pmt_no.append(i + 1)
                interest.append(Pr[i-1] * r)
                principal.append(monthly_mortgage - interest[i])
                Pr.append(Pr[i-1] - principal[i])
            row = dict(pmt_no = pmt_no[i], interest = interest[i], principal = principal[i], Pr = Pr[i])
            rows.append(row)

        # Format the amortization data into currency with commas
        rows_formatted = []
        for row in rows:
            interest = '${:,.2f}'.format(row["interest"])
            principal = '${:,.2f}'.format(row["principal"])
            Pr = '${:,.2f}'.format(row["Pr"])
            row_formatted = dict(pmt_no = row["pmt_no"], interest = interest, principal = principal, Pr = Pr)
            rows_formatted.append(row_formatted)
          
        # Return the calculated total monthly payment to the user
        return render_template("amortization.html", home_price = home_price, down_pmt = down_pmt, int_rate = int_rate, term = term,
                               P_formatted = '${:,.2f}'.format(P), monthly_mortgage_formatted = '${:,.2f}'.format(monthly_mortgage),
                               rows_formatted = rows_formatted)

    # If the user has not submitted the form, present the form to the user
    else:
        return render_template("amortization.html")
    

@app.route("/qualification/", methods=["GET", "POST"])
def qualification():
    # Calculate the user's total monthly payment

    # If request method is POST
    if request.method == "POST":
        # If field is left empty, make the default value zero (.01% for interest rate, 1 year for term)
        # Salary
        if not request.form.get("salary1"):
            salary1 = 0
        else:
            salary1 = int(request.form.get("salary1"))
        # Other Salary
        if not request.form.get("salary2"):
            salary2 = 0
        else:
            salary2 = int(request.form.get("salary2"))
        # Additional Income
        if not request.form.get("add_income"):
            add_income = 0
        else:
            add_income = int(request.form.get("add_income"))
        # Car Loan
        if not request.form.get("car_loan"):
            car_loan = 0
        else:
            car_loan = int(request.form.get("car_loan"))
        # Credit Card
        if not request.form.get("cc_pmt"):
            cc_pmt = 0
        else:
            cc_pmt = int(request.form.get("cc_pmt"))
        # Other Debts
        if not request.form.get("other_debt"):
            other_debt = 0
        else:
            other_debt = int(request.form.get("other_debt"))
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

        # Calculate the total income
        total_income = salary1 + salary2 + add_income
        # Calculate the total debt
        total_debt = car_loan + cc_pmt + other_debt

        # Calculate the two qualifying numbers that determine the max. monthly payment
        Q1 = total_income * 0.28 / 12
        Q2 = total_income * 0.36 / 12 - total_debt

        # Determine which qualifying number to use
        if Q1 <= Q2:
            total_monthly = Q1
        else:
            total_monthly = Q2
        
        # Calculate the monthly mortgage payment
        other_expenses = hoa + melloroos + prop_tax/12 + ins/12
        M = total_monthly - other_expenses
        # Calculate the monthly interest rate
        r = int_rate/100/12
        # Calculate the number of payments
        n = term * 12

        # Calculate Qualifying Loan Amount (Pq)
        Pq = M * ( (1+r)**n - 1 ) / ( r * (1+r)**n )
    
        # Return the calculated total monthly payment to the user
        return render_template("qualification.html", salary1 = salary1, salary2 = salary2, add_income = add_income,
                               car_loan = car_loan, cc_pmt = cc_pmt, other_debt = other_debt, int_rate = int_rate,
                               term = term, hoa = hoa, melloroos = melloroos, prop_tax = prop_tax, ins = ins,
                               Pq='${:,.2f}'.format(Pq))

    # If the user has not submitted the form, present the form to the user
    else:
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