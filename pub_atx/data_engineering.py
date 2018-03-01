from .app import db 
import pandas as pd
import requests
import time
from .models import Company,CompanyPrcsMnthly,CompanyPrcsDaily
import datetime
import dateutil.relativedelta
import quandl

def gather_cmpny_data():

    df_pub_atx = pd.read_csv("Austin-area-Public-Companies-2017-List.csv")

    # column_curr = df_pub_atx.columns.values.tolist()

    column_needed = ['Rank',
    'Company Name',
    'Address 1',
    'City',
    'State',
    'Zipcode',
    'Phone Number',
    'Website',    
    'Stock ticker',    
    'Year: IPO',
    'Year founded',
    'General Business Description',
    'Current top local executive',
    'Year established in Austin ',
    '2017 Austin staff',
    'Companywide employees from 10K FYE 2016',
    '[Historical] Total Local Employment, as of May 1, 2016-Q2']

    df_pub_atx = df_pub_atx[column_needed]

    df_pub_atx.fillna(0,inplace=True)

    df_pub_atx["Exch"] =  df_pub_atx["Stock ticker"].str.split(":",0).str[0].\
                                str.extract('([a-zA-Z]+)',expand=False).str.strip()

    df_pub_atx["Stock ticker"] = df_pub_atx["Stock ticker"].str.split(":",0).str[1].\
                                str.extract('([a-zA-Z]+)',expand=False).str.strip()

    df_pub_atx.columns = ['rank',\
        'name' ,\
        'address',\
        'city' ,\
        'state' ,\
        'zip_code' ,\
        'phn_nbr' ,\
        'website' ,\
        'tckr' ,\
        'ipo_yr' ,\
        'yr_founded' ,\
        'gen_buss_desc' ,\
        'curr_top_exec' ,\
        'yr_estblsh' ,\
        'austin_staff_cnt' ,\
        'comp_staff_cnt' ,\
        'tot_local_emp_cnt' ,\
        'exchng' ]

    # 1) we need to drop whole foods since it was purchased by Amazon.
    # 2) we need to drop BETR since it was purchased by Hershey Chocolate
    # 3) Cross Roads went into bankruptcy and is now CRSS, but no information out there for them...
    # 4) Victory Energy is re organizing from a exploration company to an oil field services company... thus no information out there...
    # 5) Mirna  merged with someone else and is now trading under SYBX

    df_pub_atx = df_pub_atx[(df_pub_atx.tckr != 'WFMI')] 
    df_pub_atx = df_pub_atx[(df_pub_atx.tckr != 'BETR')] 
    df_pub_atx = df_pub_atx[(df_pub_atx.tckr != 'CRDS')] 
    df_pub_atx = df_pub_atx[(df_pub_atx.tckr != 'VYEY')] 
    df_pub_atx.loc[(df_pub_atx.tckr == 'MIRN'),"tckr"]  = "SYBX"

    df_pub_atx["lat"]=""
    df_pub_atx["lng"]=""
    api_key = "AIzaSyACVuBkhxdqFNjcrqvGfo5IUGxQCrVIKxY"
    for index, row in df_pub_atx.iterrows():
        address = row['address']+', '+ row['city']+', '+ row['state']
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()
        time.sleep(1)
        if api_response_dict['status'] == 'OK':
            df_pub_atx.set_value(index,'lat', api_response_dict['results'][0]['geometry']['location']['lat'])
            df_pub_atx.set_value(index,'lng', api_response_dict['results'][0]['geometry']['location']['lng'])


    df_pub_atx['industry'] = ''
    df_pub_atx['sector'] = ''
    df_pub_atx['marketcap'] = 0

    def iex_company_request(ticker):
        iex_company_url = f'https://api.iextrading.com/1.0/stock/{ticker}/company'
        response = requests.get(iex_company_url)
        return response

    def iex_company_stat_request(ticker):
        iex_company_url = f'https://api.iextrading.com/1.0/stock/{ticker}/stats'
        response = requests.get(iex_company_url)
        return response

    for index, row in df_pub_atx.iterrows():
        ticker = df_pub_atx.loc[index, 'tckr']
        response = iex_company_request(ticker)
        if response.status_code == 200:
            response_json = response.json()
            df_pub_atx.set_value(index,'industry',response_json['industry'])
            df_pub_atx.set_value(index,'sector',response_json['sector'])
        else:
            df_pub_atx.set_value(index,'industry','unknown')
            df_pub_atx.set_value(index,'sector','unknown')


            
        response = iex_company_stat_request(ticker)
        if response.status_code == 200:
            response_json = response.json()
            df_pub_atx.set_value(index,'marketcap',response_json['marketcap'])
        else:
            df_pub_atx.set_value(index,'marketcap',0)


    df_pub_atx.to_csv("clean_company_list.csv",index=False,encoding='utf-8')


def load_tables_cmpny_data():

    df_company = pd.read_csv("clean_company_list.csv")
    data = df_company.to_dict(orient='records')
    db.engine.execute(Company.__table__.delete())
    db.engine.execute(Company.__table__.insert(),data)

    companies = db.engine.execute("select * from cmpny").fetchall()

    d1 = datetime.date.today()
    d2 = d1 - dateutil.relativedelta.relativedelta(months=36)
    start_dt = d2.strftime("%Y-%m-%d")
    end_dt = d1.strftime("%Y-%m-%d")

    quandl.ApiConfig.api_key = "bkLgy-fmbYDf_AuKMJeV"

    db.engine.execute(CompanyPrcsMnthly.__table__.delete())

    df_tckrs_nf = pd.DataFrame(["id_cmpny","tckr"])

    nf_list = []

    for company in companies:
        try:
            nf_dict = {}
            data = quandl.get("WIKI" +"/" + company.tckr,collapse="monthly", start_date=start_dt, end_date=end_dt)
            data = data.reset_index()
            data = data[['Date','Open','High','Low','Close','Volume']]
            data.columns = ["date","open","high","low","close","volume"]
            data["id_cmpny"] = company.id_cmpny
            data = data[["id_cmpny", "date","open","high","low","close","volume"]]
            data['date'] = data['date'].astype('str')
            data = data.to_dict(orient='records')
            
            db.engine.execute(CompanyPrcsMnthly.__table__.insert(),data)
        except quandl.NotFoundError as e:
            nf_dict["id_cmpny"] = company.id_cmpny
            nf_dict["tckr"] = company.tckr 
            nf_list.append(nf_dict)
            # print(company.tckr + " not found ")
            continue    

    db.engine.execute(CompanyPrcsDaily.__table__.delete())

    for company in companies:
        try:
        
            data = quandl.get("WIKI" +"/" + company.tckr, start_date=start_dt, end_date=end_dt)
            data = data.reset_index()
            data = data[['Date','Open','High','Low','Close','Volume']]
            data.columns = ["date","open","high","low","close","volume"]
            data["id_cmpny"] = company.id_cmpny
            data = data[["id_cmpny", "date","open","high","low","close","volume"]]
            data['date'] = data['date'].astype('str')
            data = data.to_dict(orient='records')
            
            db.engine.execute(CompanyPrcsDaily.__table__.insert(),data)
        except quandl.NotFoundError as e:
            # print(company.tckr + " not found ")
            continue

    stock_attributes = ["date","open","high","low","close","volume"]
    for x in nf_list:
    #     print(x["id_cmpny"])
        iex_company_url = f'https://api.iextrading.com/1.0/stock/{x["tckr"]}/chart/5y'
    #     print(iex_company_url)
        response = requests.get(iex_company_url)
        response_json = response.json()
        stock_attributes_df = pd.DataFrame.from_dict(response_json)
        df_filtered = stock_attributes_df[(stock_attributes_df.date >= start_dt) & (stock_attributes_df.date <= end_dt)]
        df_filtered_needed = df_filtered[stock_attributes]
    #     print(len(df_filtered_needed))
        data = df_filtered_needed.to_dict(orient='records')
        db.engine.execute(CompanyPrcsDaily.__table__.insert(),data)
    


