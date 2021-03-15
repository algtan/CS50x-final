For my final project in CS50x, I have created a mortgage calculator. This mortgage calculator can provide the user with 3 different calculations:

1) The monthly cost of a home
2) How much loan the user qualifies for
3) The amortization schedule of the loan

This information should help the user make an informed decision about their home purchase by letting them know how much it will cost them monthly, and how much home/loan they can reasonably afford.

To get Flask running:
1) Set FLASK_APP environment variable in the terminal
$env:FLASK_APP = "webapp"

2) Enter Virtual Environment (Windows)
env\Scripts\Activate.ps1

3) Change directory to `final_app`
(env) cd final_app

4) In the virtual environment, run the following command:
(env) python -m flask run
