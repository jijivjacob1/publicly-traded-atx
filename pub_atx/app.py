# import necessary libraries
import numpy as np
import pandas as pd
import os

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///pub_atx.sqlite"
app.config['GOOGLE_API_KEY'] = os.environ.get('GOOGLE_API_KEY', '') or ''
app.config['QUANDL_API_KEY'] = os.environ.get('QUANDL_API_KEY', '') or ''


db = SQLAlchemy(app)
from .models import Company,company_columns


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/companies')
def companies():
    results = db.session.query(*company_columns).all()

    df = pd.DataFrame(results, columns=['id_cmpny','rank','name','address','city', 'state','zip_code','phn_nbr','website',\
    'tckr','ipo_yr','yr_founded','gen_buss_desc','curr_top_exec', 'yr_estblsh','austin_staff_cnt' ,'comp_staff_cnt' ,\
    'tot_local_emp_cnt','exchng','lat','lng','industry', 'sector','marketcap'])

    return jsonify(df.to_dict(orient="records"))


'''
This function returns a python dictionary of company data from our database.
It takes one argument, a ticker symbol, that is used to look up company data.
It is used in the company overview page.
'''
def get_company_info(ticker):
    ticker = ticker.upper()
    sql_response = db.session.query(Company).filter(Company.tckr == ticker).first()
    market_cap = '${:,.2f}'.format((sql_response.marketcap))
    company_dict = {'companyName': sql_response.name,
                    'companyIndustry': sql_response.sector,
                    'companyWebsite': sql_response.website,
                    'companyDescription': sql_response.gen_buss_desc,
                    'companyTicker': sql_response.tckr,
                    'companyAddress': sql_response.address,
                    'companyExhange': sql_response.exchng,
                    'companyCEO': sql_response.curr_top_exec,
                    'companyMarketCap': market_cap,
                    'companyYear': sql_response.yr_estblsh,
                    'companyTotalStaff': sql_response.austin_staff_cnt,
                    'companyAustinStaff': sql_response.comp_staff_cnt
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
    company_data = db.session.query(Company).all()
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
