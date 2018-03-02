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


def get_company_info(ticker):
    ticker = ticker.upper()
    sql_response = db.session.query(Company).filter(Company.tckr == ticker).first()
    company_dict = {'companyName': sql_response.name,
                    'companyIndustry': sql_response.industry,
                    'tickerSymbol': sql_response.tckr,
                    'companyWebsite': sql_response.website,
                    'companyDescription': sql_response.gen_buss_desc
    }
    return company_dict

@app.route('/company/<ticker>')
def company_profile(ticker):
    company_dict = get_company_info(ticker)
    return render_template('stocks.html', **company_dict)



