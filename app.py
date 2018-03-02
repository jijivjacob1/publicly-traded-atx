import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
app = Flask(__name__)




'''
This function connects to the database
'''
def reflect_db():
    dbfile = os.path.join('db', 'pub_atx.sqlite')
    engine = create_engine(f'sqlite:///{dbfile}')
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    return Base, session


Base, session = reflect_db()

Cmpny = Base.classes.cmpny

'''
This function returns a python dictionary of company data from our database.
It takes one argument, a ticker symbol, that is used to look up company data.
It is used in the company overview page.
'''
def get_company_info(ticker):
    Base, session = reflect_db()
    Cmpny = Base.classes.cmpny
    ticker = ticker.upper()
    sql_response = session.query(Cmpny).filter(Cmpny.tckr == ticker).first()
    company_dict = {'companyName': sql_response.name,
                    'companyIndustry': sql_response.industry,
                    'companyWebsite': sql_response.website,
                    'companyDescription': sql_response.gen_buss_desc,
                    'companyTicker': sql_response.tckr
    }
    return company_dict

'''
This api route returns a semi-ordered list of all company tickers in our
database.  It is used in the company overview page.  It takes one argument, a
ticker symbol, which appears first in the array.  The remaining tickers appear
in alphabetical order.
'''
@app.route('/tickers/<ticker>')
def company_tickers_ordered(ticker):
    ticker = ticker.upper()
    company_data = session.query(Cmpny).all()
    tickers = []
    for company in company_data:
        tickers.append(company.tckr)
    tickers.sort()
    tickers.remove(ticker)
    tickers.insert(0, ticker)
    return jsonify(tickers)



'''
This api route serves up the html for the company overview pages.  It uses an
html template (stocks.html) and the get_company_info() functions to serve up
the basic structure of the page.  It takes one argument, a ticker symbol, which
designates which company the page analyzes.
'''
@app.route("/company/<ticker>")
def company_profile(ticker):
    company_dict = get_company_info(ticker)
    return render_template('stocks.html', **company_dict)



if __name__ == "__main__":
    app.run(debug=True)
