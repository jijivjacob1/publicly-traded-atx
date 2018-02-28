# import necessary libraries
import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

from flask import (
    Flask,
    render_template,
    jsonify)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///pub_atx.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

cmpny = Base.classes.cmpny

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

sel = [cmpny.id_cmpny ,
    cmpny.rank ,
    cmpny.name,
    cmpny.address ,
    cmpny.city ,
    cmpny.state ,
    cmpny.zip_code,
    cmpny.phn_nbr,
    cmpny.website ,
    cmpny.tckr ,
    cmpny.ipo_yr,
    cmpny.yr_founded ,
    cmpny.gen_buss_desc ,
    cmpny.curr_top_exec,
    cmpny.yr_estblsh ,
    cmpny.austin_staff_cnt ,
    cmpny.comp_staff_cnt ,
    cmpny.tot_local_emp_cnt ,
    cmpny.exchng ,
    cmpny.lat ,
    cmpny.lng ,
    cmpny.industry ,
    cmpny.sector ,
    cmpny.marketcap ]

@app.route('/companies')
def metadata():


    results = session.query(*sel).all()

    df = pd.DataFrame(results, columns=['id_cmpny' ,
    'rank' ,
    'name',
    'address' ,
    'city' ,
    'state' ,
    'zip_code',
    'phn_nbr',
    'website' ,
    'tckr' ,
    'ipo_yr',
    'yr_founded' ,
    'gen_buss_desc' ,
    'curr_top_exec',
    'yr_estblsh' ,
    'austin_staff_cnt' ,
    'comp_staff_cnt' ,
    'tot_local_emp_cnt' ,
    'exchng' ,
    'lat' ,
    'lng' ,
    'industry' ,
    'sector' ,
    'marketcap'])

    return jsonify(df.to_dict(orient="records"))

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # WARNING! Don't use debug in heroku!
    app.run(debug=True)
    # app.run()