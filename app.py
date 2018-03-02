import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
app = Flask(__name__)





#################################################
# Database Setup
#################################################
def reflect_db():
    dbfile = os.path.join('db', 'pub_atx.sqlite')
    engine = create_engine(f'sqlite:///{dbfile}')
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)
    return Base, session


Base, session = reflect_db()

Cmpny = Base.classes.cmpny


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


@app.route("/company/<ticker>")
def company_profile(ticker):
    company_dict = get_company_info(ticker)
    return render_template('stocks.html', **company_dict)



if __name__ == "__main__":
    app.run(debug=True)
