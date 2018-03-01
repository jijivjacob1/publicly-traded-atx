from .app import db 


class Company(db.Model):
    __tablename__ = 'cmpny'
    
    id_cmpny = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    name = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zip_code = db.Column(db.Text)
    phn_nbr = db.Column(db.Text)
    website = db.Column(db.Text)
    tckr = db.Column(db.Text)
    ipo_yr = db.Column(db.Integer)
    yr_founded = db.Column(db.Integer)
    gen_buss_desc = db.Column(db.Text)
    curr_top_exec = db.Column(db.Text)
    yr_estblsh = db.Column(db.Integer)
    austin_staff_cnt = db.Column(db.Float)
    comp_staff_cnt = db.Column(db.Float)
    tot_local_emp_cnt = db.Column(db.Float)
    exchng = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    industry = db.Column(db.Text)
    sector = db.Column(db.Text)
    marketcap = db.Column(db.Float)
    
  
    
class CompanyPrcsMnthly(db.Model):
    __tablename__ = 'cmpny_prcs_mnthly'
    
    id_cmpny_prcs_mnthly = db.Column(db.Integer, primary_key=True)
    id_cmpny = db.Column(db.Integer)
    date = db.Column(db.Text)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    
    
    def __repr__(self):
        return f"id={self.id_cmpny_prcs_mnthly},name=[self.id_cmpny]"
    
class CompanyPrcsDaily(db.Model):
    __tablename__ = 'cmpny_prcs_daily'
    
    id_cmpny_prcs_daily = db.Column(db.Integer, primary_key=True)
    id_cmpny = db.Column(db.Integer)
    date = db.Column(db.Text)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)

company_columns = [ Company.id_cmpny ,
    Company.rank,
    Company.name ,
    Company.address,
    Company.city ,
    Company.state ,
    Company.zip_code ,
    Company.phn_nbr ,
    Company.website ,
    Company.tckr ,
    Company.ipo_yr ,
    Company.yr_founded ,
    Company.gen_buss_desc ,
    Company.curr_top_exec ,
    Company.yr_estblsh ,
    Company.austin_staff_cnt ,
    Company.comp_staff_cnt ,
    Company.tot_local_emp_cnt ,
    Company.exchng ,
    Company.lat ,
    Company.lng ,
    Company.industry ,
    Company.sector ,
    Company.marketcap]
